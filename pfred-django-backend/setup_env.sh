# export PERL5LIB="/usr/local/lib64/perl5/"
# export PERL5LIB="${PERL5LIB}:/usr/lib64/perl5/"
# export PERL5LIB="${PERL5LIB}:${PFRED_HOME}/BioPerl-1.6.1"
# export PERL5LIB="${PERL5LIB}:${ENSEMBL_API}/ensembl/modules"
# export PERL5LIB="${PERL5LIB}:${ENSEMBL_API}/ensembl-compara/modules"
# export PERL5LIB="${PERL5LIB}:${ENSEMBL_API}/ensembl-variation/modules"
# export PERL5LIB="${PERL5LIB}:${ENSEMBL_API}/ensembl-functgenomics/modules"

# User specific environment and startup programs
export PFRED_HOME="/home/pfred"
export SCRIPTS_DIR="${PFRED_HOME}/scripts/pfred"
export RUN_DIR="/home/pfred/scratch"
export BOWTIE_HOME="${PFRED_HOME}/scripts/bowtie"
export BOWTIE="${BOWTIE_HOME}/bowtie"
export BOWTIE_INDEXES="${BOWTIE_HOME}/indexes"
export BOWTIE_BUILD="${BOWTIE_HOME}/bowtie-build"
export PERL5LIB=$SCRIPTS_DIR

# #path
# export PATH=${CATALINA_HOME}/bin:$HOME/bin:${PFRED_HOME}/scripts/pfred:$PATH