#Max Simlutaneos Threads
maxthreads = 5

# Rsync Binary
rsync_bin = '/usr/local/bin/rsync'

#Rsync options
rsync_options = '-rtv --delete -e "ssh -p 5252"'

#List of locations and destiny

location_list = []
location_list.append(
    {
        "nome": "acicredi",
        "origin": "10.139.0.10:/mnt/dadosacicredi01/share",
        "destin": "/mnt/dadosarcom/backuparquivos/acicredi/lnx01410400/",
    }
)
