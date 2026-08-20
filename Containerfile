# Formwork (ERP) image — ERPNext + branboos_erp, layered on Frappe's
# own published base images per implementation appendix §5.
#
# Adapted from frappe_docker's images/layered/Containerfile:
#   https://github.com/frappe/frappe_docker/blob/main/images/layered/Containerfile
# `frappe/build` and `frappe/base` are Frappe's own maintained Docker Hub
# images — this file intentionally does not reinvent nginx/wkhtmltopdf/node
# setup, per the appendix's "don't build Frappe's deployment from scratch"
# guidance.
#
# Build context must be the workspace root (parent of branboos-structura/
# and branboos-erp/) so this Containerfile can COPY the local
# branboos_erp source — see deploy/docker-compose.yml.
#
# apps.json (erpnext) is fetched from GitHub as usual, via a BuildKit
# secret so no token/URL ends up baked into image layer history:
#   docker build --secret=id=apps_json,src=branboos-erp/apps.json ...
#
# branboos_erp itself is added from the local build context rather
# than a git URL, because this repo hasn't been pushed to a remote yet.
# Once it has, replace the COPY + `bench get-app <local path>` step below
# with a second entry in apps.json (url + branch) — the same mechanism
# used for erpnext — and drop the COPY.

ARG FRAPPE_BRANCH=version-16
ARG FRAPPE_IMAGE_PREFIX=frappe

FROM ${FRAPPE_IMAGE_PREFIX}/build:${FRAPPE_BRANCH} AS builder

ARG FRAPPE_BRANCH=version-16
ARG FRAPPE_PATH=https://github.com/frappe/frappe
ARG CACHE_BUST=""

USER frappe

RUN --mount=type=secret,id=apps_json,target=/opt/frappe/apps.json,uid=1000,gid=1000 \
  : "${CACHE_BUST}" && \
  export APP_INSTALL_ARGS="" && \
  if [ -f /opt/frappe/apps.json ] && [ -s /opt/frappe/apps.json ]; then \
    export APP_INSTALL_ARGS="--apps_path=/opt/frappe/apps.json"; \
  fi && \
  bench init ${APP_INSTALL_ARGS}\
    --frappe-branch=${FRAPPE_BRANCH} \
    --frappe-path=${FRAPPE_PATH} \
    --no-procfile \
    --no-backups \
    --skip-redis-config-generation \
    --verbose \
    /home/frappe/frappe-bench && \
  cd /home/frappe/frappe-bench && \
  echo "{}" > sites/common_site_config.json && \
  find apps -mindepth 1 -path "*/.git" | xargs rm -fr

# ── Layer in branboos_erp from the local build context ────────────────
COPY --chown=frappe:frappe branboos-erp /home/frappe/branboos_erp_src
RUN cd /home/frappe/frappe-bench && \
  bench get-app --skip-assets /home/frappe/branboos_erp_src && \
  rm -rf /home/frappe/branboos_erp_src apps/branboos_erp/.git && \
  bench build

FROM ${FRAPPE_IMAGE_PREFIX}/base:${FRAPPE_BRANCH} AS backend

USER frappe

COPY --from=builder --chown=frappe:frappe /home/frappe/frappe-bench /home/frappe/frappe-bench

WORKDIR /home/frappe/frappe-bench

# Move assets to image-layer storage
RUN cp -r /home/frappe/frappe-bench/sites/assets /home/frappe/frappe-bench/assets && \
  rm -rf /home/frappe/frappe-bench/sites/assets

VOLUME [ \
  "/home/frappe/frappe-bench/sites", \
  "/home/frappe/frappe-bench/logs" \
]

USER root
COPY branboos-erp/resources/core/main-entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod 755 /usr/local/bin/entrypoint.sh

COPY branboos-erp/resources/core/start.sh /usr/local/bin/start.sh
RUN chmod 755 /usr/local/bin/start.sh

USER frappe
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

CMD ["start.sh"]
