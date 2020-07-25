FROM python:alpine
WORKDIR /app
COPY reset-all.py .
RUN pip install --no-cache-dir requests
ENV CONTROLLER=localhost \
    USERNAME=admin \
    PASSWORD= \
    PORT=8443 \
    STEP=4 \
    MODULUS=0 \
    TYPE=uap \
    VERIFY_SSL=false
CMD python ./reset-all.py --controller ${CONTROLLER} --username ${USERNAME} --password ${PASSWORD} --port ${PORT} --step ${STEP} --modulus ${MODULUS} --type ${TYPE} --verify ${VERIFY_SSL}
