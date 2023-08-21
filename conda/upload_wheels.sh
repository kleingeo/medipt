# Modified from pandas's https://github.com/pandas-dev/pandas/blob/main/ci/upload_wheels.sh

set_upload_vars() {
#    echo "IS_PUSH is $IS_PUSH"
#    echo "IS_SCHEDULE_DISPATCH is $IS_SCHEDULE_DISPATCH"

    echo push and tag event
    export ANACONDA_UPLOAD="true"
    export

}
upload_wheels() {
    echo ${PWD}
    if [[ ${ANACONDA_UPLOAD} == true ]]; then
        if [ -z ${ANACONDA_TOKEN} ]; then
            echo no token set, not uploading
        else
            # sdists are located under dist folder when built through setup.py
            if compgen -G "./dist/*.gz"; then
                echo "Found sdist"
                anaconda -q -t ${ANACONDA_TOKEN} upload --force ./dist/*.gz
                echo "Uploaded sdist"
            fi
            if compgen -G "./wheelhouse/*.whl"; then
                echo "Found wheel"
                anaconda -q -t ${ANACONDA_TOKEN} upload --force ./wheelhouse/*.whl
                echo "Uploaded wheel"
            fi
#            echo "PyPI-style index: https://pypi.anaconda.org/$ANACONDA_ORG/simple"
        fi
    fi
}