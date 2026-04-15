"""
Task 2: Iterative Min-Max
Single-pass algorithm that maintains current_min and current_max.
Comparison count expected: 2n - 2
No built-in min(), max(), or sort() used.
"""


class IterativeMinMax:
    """
    Finds minimum and maximum using a single linear scan.

    Algorithm:
        - Initialise min and max to the first element.
        - For every subsequent element, compare against current_min
          and current_max (2 comparisons per element).
        - Total comparisons: 2(n-1) = 2n - 2
    """

    def __init__(self):
        self.comp_count = 0  # manual comparison counter

    def find(self, data):
        """
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

        current_min = data[0]
        current_max = data[0]

        for i in range(1, len(data)):
            # Comparison 1: is data[i] less than current minimum?
            self.comp_count += 1
            if data[i] < current_min:
                current_min = data[i]

            # Comparison 2: is data[i] greater than current maximum?
            self.comp_count += 1
            if data[i] > current_max:
                current_max = data[i]

        return current_min, current_max, self.comp_count


#  quick self-test 
if __name__ == "__main__":
    sample = [3.5, -1.2, 7.8, 2.0, 9.1, -5.5, 4.4]
    algo = IterativeMinMax()
    mn, mx, comps = algo.find(sample)
    n = len(sample)
    print(f"Data        : {sample}")
    print(f"Min         : {mn}")
    print(f"Max         : {mx}")
    print(f"Comparisons : {comps}  (expected 2n-2 = {2*n - 2})")
