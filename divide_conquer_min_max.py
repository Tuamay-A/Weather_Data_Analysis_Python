"""
Task 3: Divide & Conquer Min-Max
Recursive approach following T(n) = 2T(n/2) + 2.
Comparison count expected: 3n/2 - 2  (for n that is a power of 2)
No built-in min(), max(), or sort() used.
"""


class DivideConquerMinMax:
    """
    Finds minimum and maximum using divide & conquer.

    Recurrence:  T(n) = 2T(n/2) + 2
    Solved:      T(n) = 3n/2 - 2   comparisons

    Why fewer comparisons than iterative?
        Iterative checks each element twice (vs min AND vs max) = 2(n-1).
        D&C pairs up elements first, then propagates only the smaller
        upward for min-tracking and the larger for max-tracking,
        saving roughly n/2 comparisons overall.
    """

    def __init__(self):
        self.comp_count = 0  # manual comparison counter

    def find(self, data):
        """
        Public entry point.

        Parameters
        ----------
        data : list of float

        Returns
        -------
        (min_val, max_val, comp_count)
        """
        if not data:
            raise ValueError("Dataset is empty.")

        self.comp_count = 0
        mn, mx = self._find_min_max(data, 0, len(data) - 1)
        return mn, mx, self.comp_count

    def _find_min_max(self, arr, low, high):
        """
        Recursive worker.

        Base cases
        ----------
        1 element  : min == max, no comparison needed.
        2 elements : 1 comparison to decide which is min and which is max.

        Recursive step
        --------------
        Split at mid, recurse on [low..mid] and [mid+1..high],
        then merge with 2 comparisons (left_min vs right_min,
        left_max vs right_max).
        """
        #  Base case 1: single element 
        if low == high:
            return arr[low], arr[low]

        #  Base case 2: two elements 
        if high == low + 1:
            self.comp_count += 1          # one comparison for 2 elements
            if arr[low] < arr[high]:
                return arr[low], arr[high]
            else:
                return arr[high], arr[low]

        #  Recursive step 
        mid = (low + high) // 2

        left_min,  left_max  = self._find_min_max(arr, low,     mid)
        right_min, right_max = self._find_min_max(arr, mid + 1, high)

        # Merge: 2 comparisons to combine results
        self.comp_count += 1
        overall_min = left_min if left_min < right_min else right_min

        self.comp_count += 1
        overall_max = left_max if left_max > right_max else right_max

        return overall_min, overall_max


#  quick self-test 
if __name__ == "__main__":
    sample = [3.5, -1.2, 7.8, 2.0, 9.1, -5.5, 4.4, 6.6]   # n=8 (power of 2)
    algo = DivideConquerMinMax()
    mn, mx, comps = algo.find(sample)
    n = len(sample)
    import math
    expected = (3 * n) // 2 - 2
    print(f"Data        : {sample}")
    print(f"Min         : {mn}")
    print(f"Max         : {mx}")
    print(f"Comparisons : {comps}  (expected 3n/2-2 = {expected} for n={n})")
