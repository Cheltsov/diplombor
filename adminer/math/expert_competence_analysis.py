import numpy as np
from adminer.math.modules.CompetenceExpert import CompetenceExpert


def mainer():
    r = CompetenceExpert(id_poll=31)
    r.main()

    list_m = np.array(r.list_m)
    list_q = np.array(r.list_q)
    list_s = np.array(r.list_s)
    list_rank = np.array(r.rank_q)

    l = r.getMark()
    exit()
