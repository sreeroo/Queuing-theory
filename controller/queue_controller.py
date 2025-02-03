from model.mm1_queue import MM1Queue


class QueueController:
    def __init__(self, input_frame, result_frame, plot_frame):
        self.input_frame = input_frame
        self.result_frame = result_frame
        self.plot_frame = plot_frame
        self.current_model = None

    def handle_calculation(self, params):
        try:
            self.current_model = MM1Queue(params['arrival_rate'], params['service_rate'])
            results = self._prepare_results(params.get('n'))
            self.result_frame.update_results(results)
            self.plot_frame.update_plots(self.current_model, params.get('n'))
        except ValueError as e:
            self.input_frame._show_error(str(e))

    def _prepare_results(self, n=None):
        results = {
            'utilization': self.current_model.utilization,
            'avg_system': self.current_model.avg_system_customers,
            'avg_queue': self.current_model.avg_queue_length,
            'time_system': self.current_model.avg_time_system,
            'waiting_time': self.current_model.avg_waiting_time,
        }
        if n is not None:
            results['prob_n'] = self.current_model.probability(n)
        return results