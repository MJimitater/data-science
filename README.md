# IDS-1

This repo is meant to analyse the Ringelmann effect on different-sized co-editing networks, as found in git repos.

`main.ipynb` contains code for manually building a multiple linear regression analysis.

`visualization.ipynb` contains all the code to visualize the mined data (the code snippets orginate from the git2net tutorial)

`main_tlp.ipynb` contains code for building a multiple linear regression analysis of the git2net-mined `tlp`-repo with `statsmodels`.

`main_hello-world.ipynb` contains code for building a multiple linear regression analysis of the git2net-mined `hello-world`-repo with`statsmodels`.

`main_architecture.ipynb` contains code for building a multiple linear regression analysis of the git2net-mined `android-architecture`-repo with `statsmodels`.

`main_nginx.ipynb` contains code for building a multiple linear regression analysis of the git2net-mined `nginx-proxy`-repo with `statsmodels`.

## Usage

- Install the `git2net` package (pip install git2net)
- Git clone the desired repo that you wish to analyse the co-editing network of.
- Pick one of the `main` codes.. the above ones are fitted for chosen repos.
- Mine the repo by uncommenting the mining block in the `main` code and specifying `repo_dir` (location of stored git repo) and `sqlite_db_file` (location of database file that will be mined in the `main` code.).
- Run the `main` code and analyse in respect to the Ringelmann effect.

