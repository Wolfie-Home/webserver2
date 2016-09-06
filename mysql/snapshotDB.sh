!# /bin/bash
mysqldump --events --routines --triggers -u wolfie -pdummypass wolfie_home > 'DB.mysql'
