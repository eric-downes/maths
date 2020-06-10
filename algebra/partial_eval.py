'''
matrix multiplication (2 x 4)(4 x 1) is defined
but of course (2 x 4)(5 x 1) is not

... lets change that

(what space does this map into... space of functions of linear transforms I think C + XR...

image in terms of area mappings & rotations
image in space of eigenvalues?
image in space of graphs?
image in QM? -- O(x)|psi> = |psi'>(x)

'''
import numpy as np
import warnings

def partial_matmul(A, B, how='inside') -> Callable:
    # need to call back into this ... develop object model
    if how != 'inside':
        raise NotImplementedError('Only inside inserts supported at this time')    
    if len(np.shape(A)) < 2: A = A.reshape(np.shape(A)[0], 1)
    if len(np.shape(B)) > 2 or len(np.shape(B)) > 2:
        raise NotImplementedError('No ND-array support at this time for N!=2')
    a = np.shape(A)[1]
    b = np.shape(B)[0]
    d = a - b
    if d < 0:
        R = B[a:, :]
        C = np.matmul(A, B[:a, :])
        def partmatmul(x):
            return C + np.matmul(x, R)
    elif d > 0:
        R = A[:, b:]
        C = np.matmul(A[:, :b], B)
        def partmatmul(x):
            return C + np.matmul(R, x)
    return partmatmul

                            
