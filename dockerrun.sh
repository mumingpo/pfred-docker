docker run \
    -it \
    -p 8000:8000 \
    --rm \
    --name pfred \
    --mount "type=bind,source=$(pwd)/pfred-django-backend,target=/home/pfred" \
    --workdir "/home/pfred" \
    continuumio/miniconda3:23.9.0-0
    bash
