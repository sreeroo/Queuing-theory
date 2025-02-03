class MM1Queue:
    def __init__(self, arrival_rate: float, service_rate: float):
        self.λ = arrival_rate
        self.μ = service_rate
        self.validate_parameters()

    def validate_parameters(self):
        if self.λ <= 0 or self.μ <= 0:
            raise ValueError("Raten müssen positive Zahlen sein")
        if self.λ >= self.μ:
            raise ValueError("Ankunftsrate muss kleiner als Bedienrate sein")

    @property
    def utilization(self) -> float:
        return self.λ / self.μ

    @property
    def avg_system_customers(self) -> float:
        return self.utilization / (1 - self.utilization)

    @property
    def avg_queue_length(self) -> float:
        return (self.utilization ** 2) / (1 - self.utilization)

    @property
    def avg_time_system(self) -> float:
        return 1 / (self.μ - self.λ)

    @property
    def avg_waiting_time(self) -> float:
        return self.λ / (self.μ * (self.μ - self.λ))

    def probability(self, n: int) -> float:
        return (1 - self.utilization) * (self.utilization ** n)