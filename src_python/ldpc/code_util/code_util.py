import numpy as np
from itertools import combinations
import ldpc.mod2
import scipy.sparse
from scipy.special import comb as nCr
from typing import Union, Tuple, List

def construct_generator_matrix(pcm: Union[np.ndarray, scipy.sparse.spmatrix]) -> scipy.sparse.spmatrix:
    '''
    Constructs a generator matrix G from a given parity check matrix H. 
    The generator matrix G is formed such that it satisfies the condition H * G.T = 0 (mod 2), 
    where G.T represents the transpose of G and the multiplication is carried out in GF(2).

    Each row of the generator matrix G is a vector in the null space of H, 
    meaning that when matrix H is multiplied by any of these vectors, 
    the result is a zero vector, satisfying the parity check condition.

    Parameters
    ----------
    pcm : Union[np.ndarray, scipy.sparse.spmatrix]
        A binary matrix representing the parity check matrix H, 
        which can be either a dense numpy array or a sparse matrix.

    Returns
    -------
    scipy.sparse.spmatrix
        The generator matrix G as a sparse matrix, which provides efficient storage 
        and performance for matrices that are large or have a high sparsity.

    Examples
    --------
    >>> H = np.array([[0, 0, 0, 1, 1, 1, 1],
                      [0, 1, 1, 0, 0, 1, 1],
                      [1, 0, 1, 0, 1, 0, 1]])
    >>> G = construct_generator_matrix(H)
    >>> assert (H @ G.T % 2).nnz == 0  # Verifying that H * G.T is a zero matrix in GF(2)
    >>> print(G.toarray())  # Convert the sparse matrix G to a dense array for printing
    [[1 1 1 0 0 0 0]
     [0 1 1 1 1 0 0]
     [0 1 0 1 0 1 0]
     [0 0 1 1 0 0 1]]

    Note
    ----
    The function assumes that the input matrix H is a valid parity check matrix 
    and does not perform any checks for this condition. It is the user's responsibility 
    to ensure that H is properly formed.

    The function uses the `mod2.nullspace` method from the `ldpc` package to find the null space.

    '''
    return ldpc.mod2.nullspace(pcm)

def estimate_min_distance(pcm: Union[scipy.sparse.spmatrix,np.ndarray], timeout_seconds: float = 0.025, number_of_words_to_save = 10):

    """
    Estimates the code distance of a given parity check matrix (pcm).

    This function first calculates the the kernel of the parity matrix to obtain a basis of the codewords. It then searches over
    random linear combinations of the basis to find codewords with low weight. The `timeout_seconds` parameter controls the maximum
    amount of time the function spends looking for low-weight codewords.

    Parameters
    ----------
    pcm : Union[scipy.sparse.spmatrix,np.ndarray]
        The parity check matrix to estimate the code distance for.
    timeout_seconds : float, optional
        The maximum amount of time to spend estimating the code distance. Defaults to 0.025.
    number_of_words_to_save : int, optional
        The number of minimum weight words to save. Defaults to 10.

    Returns
    -------
    tuple
        A tuple containing the estimated minimum distance (int), the number of samples searched (int), 
        and a Scipy sparse matrix of the minimum weight words.
    """

    return ldpc.mod2.estimate_code_distance(pcm, timeout_seconds, number_of_words_to_save)

def compute_code_dimension(pcm: Union[scipy.sparse.spmatrix,np.ndarray]) -> int:
    """
    Compute the code dimension of a given parity check matrix.

    This function computes the code dimension of the parity check matrix (pcm) using the Rank-Nullity theorem.
    According to the Rank-Nullity theorem, the dimension of the code (k) is given by k = n - rank(pcm), where n is the number of columns in the pcm.

    Parameters
    ----------
    pcm : Union[scipy.sparse.spmatrix, np.ndarray]
        The parity check matrix to compute the code dimension for.

    Returns
    -------
    int
        The code dimension of the parity check matrix.
    """
    return pcm.shape[1] - ldpc.mod2.rank(pcm, method="dense")

def compute_code_parameters(pcm: Union[scipy.sparse.spmatrix,np.ndarray], timeout_seconds: float = 0.025) -> Tuple[int, int, int]:
    """
    Compute the parameters of a given parity check matrix.

    This function computes the parameters of the parity check matrix (pcm), including the number of columns (n), 
    the code dimension (k), and an estimate of the minimum distance.

    Parameters
    ----------
    pcm : Union[scipy.sparse.spmatrix, np.ndarray]
        The parity check matrix to compute the parameters for.
    timeout_seconds : float, optional
        The maximum amount of time to spend estimating the minimum distance. Defaults to 0.025.

    Returns
    -------
    Tuple[int, int, int]
        A tuple containing the number of columns (n), the code dimension (k), and the estimated minimum distance.
    """
    n = pcm.shape[1]
    k = compute_code_dimension(pcm)
    distance_estimate,_,_=estimate_min_distance(pcm, timeout_seconds)

    return (n,k,distance_estimate)

# def codewords(H):
#     '''
#     Computes all of the the codewords of the code corresponding to the parity check matrix H. The codewords are given by the span of the nullspace.

#     Parameters
#     ----------

#     H: numpy.ndarray
#         A parity check matrix.

#     Returns
#     -------
#     numpy.ndarray
#         A matrix where each row corresponds to a codeword

#     Note
#     ----
#     If you want to calculate a basis of the codewords use `ldpc.mod2.nullspace`.

#     Examples
#     --------
#     >>> H=np.array([[0, 0, 0, 1, 1, 1, 1],[0, 1, 1, 0, 0, 1, 1],[1, 0, 1, 0, 1, 0, 1]])
#     >>> print(codewords(H))
#     [[0 0 0 0 0 0 0]
#      [0 0 0 1 1 1 1]
#      [0 0 1 0 1 1 0]
#      [0 0 1 1 0 0 1]
#      [0 1 0 0 1 0 1]
#      [0 1 0 1 0 1 0]
#      [0 1 1 0 0 1 1]
#      [0 1 1 1 1 0 0]
#      [1 0 0 0 0 1 1]
#      [1 0 0 1 1 0 0]
#      [1 0 1 0 1 0 1]
#      [1 0 1 1 0 1 0]
#      [1 1 0 0 1 1 0]
#      [1 1 0 1 0 0 1]
#      [1 1 1 0 0 0 0]
#      [1 1 1 1 1 1 1]]
#     '''

#     if(isinstance(H, scipy.sparse.spmatrix)):
#         H = H.toarray()

#     _, n = H.shape
#     zero_cw = np.zeros(n).astype(int)  # zero codewords
#     cw = row_span(nullspace(H))  # nonzero codewords
#     cw = np.vstack([zero_cw, cw])

#     return cw

def search_cycles(H, girth,row=None,terminate=True,exclude_rows=[]):

    """
    Searches (and counts) cycles of a specified girth.

    Parameters
    ----------

    H: numpy.ndarray
        The parity check matrix
    girth: int
        The girth (length) of the code cycles to search for
    row: int, optional
        Default value is None. If a row is specified, the function returns the local girth for that row. If row=None, then the global girth is calculated.
    terminate: int, optional
        Default value is True. If set to True, the search function will terminate as soon as the first cycle of the specefied girth is found
    exclude_rows: list, optional
        The rows of the parity check to ignore. This is useful when you are filling an empty matrix.
    
    Returns
    -------
    bool, if Terminate=True
        True if a cycle of specified girth is found. False if no cycles are found.
    int, if Terminate=False
        If terminate is set to true, the function will count the number of cycles of the specified girth
    """

    if(isinstance(H, scipy.sparse.spmatrix)):
        H = H.toarray()

    m, n = np.shape(H)
    cycle_count = 0

    if row is None:
        print(girth)
        print(list(combinations([k for k in range(m)], girth // 2)))
        for i, combination in enumerate(combinations([k for k in range(m)], girth // 2)):
            row_sum = np.zeros(n).astype(int)
            for _, element in enumerate(combination):
                row_sum += H[element]
            two_count = np.count_nonzero(row_sum == 2)
            if two_count >= girth // 2:
                if terminate: return True
                cycle_count += nCr(two_count, girth // 2) 
    else:
        rows=[row]+exclude_rows
        for i, combination in enumerate(combinations([k for k in range(m) if k not in rows], (girth // 2)-1)):
            row_sum = np.zeros(n).astype(int)
            temp=(row,)+combination
            for _, element in enumerate(temp):
                row_sum += H[element]

            two_count = np.count_nonzero(row_sum == 2)
            if two_count >= girth // 2:
                if terminate: return True
                cycle_count += nCr(two_count, girth // 2)     

    if terminate: return False #terminates if the code is not cycle free
    return cycle_count



def compute_column_row_weights(H):

    """
    Returns the upper bounds on the row and column weights of parity check matrix

    Parameters
    ----------

    H: numpy.ndarray
        The parity check matrix

    Returns
    -------
    int
        The maximum column-weight
    int
        The maximum row-weight
    """

    if(isinstance(H, scipy.sparse.spmatrix)):
        H = H.toarray()

    return np.sum(H,axis=0), np.sum(H,axis=1)

def get_ldpc_params(H):

    """
    Returns the upper bounds on the row and column weights of parity check matrix

    Parameters
    ----------

    H: numpy.ndarray
        The parity check matrix

    Returns
    -------
    int
        The maximum column-weight
    int
        The maximum row-weight
    """

    if(isinstance(H, scipy.sparse.spmatrix)):
        H = H.toarray()

    cols, rows = compute_column_row_weights(H)

    return np.max(cols), np.max(rows)

