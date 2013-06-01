#!/usr/bin/env python
"""
ezscatter: helper script for pyina.mpi maps using the 'scatter gather' strategy
(same exact code as ezpool, but uses pyina.mpi_scatter)

This is a helper script for pyina's mpi.Mapper class. Don't use it directly.
"""

import logging
log = logging.getLogger("ezscatter")
log.addHandler(logging.StreamHandler())
def _debug(boolean):
    """print debug statements"""
    if boolean: log.setLevel(logging.DEBUG)
    else: log.setLevel(logging.WARN)
    return


if __name__ == '__main__':

    from pyina.mpi_scatter import parallel_map
    import dill as pickle
    import sys
    from pyina import mpi
    world = mpi.world

    funcname = sys.argv[1]
    argfilename = sys.argv[2]
    outfilename = sys.argv[3]

    if funcname.endswith('.pik'):  # used pickled func
        workdir = None
        func = pickle.load(open(funcname,'r'))
    else:  # used tempfile for func
        workdir = sys.argv[4]
        sys.path = [workdir] + sys.path
        module = __import__(funcname)
        sys.path.pop(0)
        func = module.FUNC
    args,kwds = pickle.load(open(argfilename,'r'))

    if world.rank == 0:
        log.info('funcname: %s' % funcname)        # sys.argv[1]
        log.info('argfilename: %s' % argfilename)  # sys.argv[2] 
        log.info('outfilename: %s' % outfilename)  # sys.argv[3]
        log.info('workdir: %s' % workdir)          # sys.argv[4]
        log.info('func: %s' % func)
        log.info('args: %s' % str(args))
        log.info('kwds: %s' % str(kwds))
    res = parallel_map(func, *args, **kwds) #XXX: called on ALL nodes ?

    if world.rank == 0:
        log.info('res: %s' % str(res))
        pickle.dump(res, open(outfilename,'w'))


# end of file
