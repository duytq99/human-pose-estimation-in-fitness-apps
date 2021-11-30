class RepetitionCounter():
    def __init__(self, enter_threshold=0.8, exit_threshold=0.2):
        self._enter_threshold = enter_threshold
        self._exit_threshold = exit_threshold
        self._pose_entered = False
        self._n_repeats = 0
    @property
    def n_repeats(self):
        return self._n_repeats
    def fit(self, data):
        pose_confidence = 0.0
        if data is not None:
            pose_confidence = data
        if not self._pose_entered:
            self._pose_entered = pose_confidence > self._enter_threshold
            return self._n_repeats
        if pose_confidence < self._exit_threshold:
            self._n_repeats += 1
            self._pose_entered = False
        return self._n_repeats