import os
import matplotlib.pyplot as plt
import numpy as np

class TrendVisualizer:
    def __init__(self):
        self.reports_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'reports', 'trends'))
        os.makedirs(self.reports_dir, exist_ok=True)
        
    def generate_forecast_chart(self, history: np.ndarray, forecast: np.ndarray, lower: np.ndarray, upper: np.ndarray):
        """
        Creates a time-series line chart showing the past and forecasting the future
        with a shaded confidence interval region.
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # History (Security Score)
        hist_len = len(history)
        ax.plot(range(hist_len), history[:, 0], label="Historical Security Score", color='blue', marker='o')
        
        # Forecast
        forecast_len = len(forecast)
        x_forecast = range(hist_len - 1, hist_len + forecast_len - 1)
        
        # We start forecast plot from the last history point to connect the lines
        f_line = [history[-1, 0]] + list(forecast[:, 0])
        l_line = [history[-1, 0]] + list(lower[:, 0])
        u_line = [history[-1, 0]] + list(upper[:, 0])
        
        ax.plot(x_forecast, f_line, label="Forecasted Score", color='orange', linestyle='--')
        ax.fill_between(x_forecast, l_line, u_line, color='orange', alpha=0.2, label="90% Confidence Interval")
        
        ax.set_title('Security Score Trend Forecast (LSTM)')
        ax.set_xlabel('Time Steps')
        ax.set_ylabel('Security Score')
        ax.set_ylim(0, 100)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plot_path = os.path.join(self.reports_dir, "score_forecast_ci.png")
        fig.savefig(plot_path, bbox_inches='tight', dpi=300)
        plt.close(fig)
        return plot_path
