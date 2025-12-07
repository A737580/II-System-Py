import numpy as np

class SugenoLeastSquaresTrainer1D:
    def __init__(self, model, epsilon=1e-6):
        self.model = model
        self.epsilon = epsilon

    def train(self, data):
        R = len(self.model.rules)
        N = len(data)

        Phi = np.zeros((N, 2 * R))
        Y = np.zeros(N)

        for i, sample in enumerate(data):
            x, y = sample.x, sample.y

            weights = np.array([r.firing_strength(x) for r in self.model.rules])
            w_sum = weights.sum()

            if w_sum == 0:
                continue

            weights /= w_sum

            row = []
            for w in weights:
                row.extend([w * x, w])

            Phi[i, :] = row
            Y[i] = y

        # МНК: theta = (ΦᵀΦ)^(-1) Φᵀ y
        theta = np.linalg.pinv(Phi.T @ Phi) @ Phi.T @ Y

        # записываем коэффициенты обратно в правила
        for i, rule in enumerate(self.model.rules):
            rule.a = theta[2 * i]
            rule.b = theta[2 * i + 1]
