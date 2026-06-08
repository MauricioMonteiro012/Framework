from flask import jsonify
from Application.Service.dashboard_service import DashboardService


class DashboardController:

    @staticmethod
    def get_dashboard(current_user):
        try:
            data = DashboardService.get_dashboard(current_user.id)
            return jsonify(data), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400