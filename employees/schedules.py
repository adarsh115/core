from employees.services import AutomatedPayrollService
from background_task import background


@background
def run_payroll_service():
    service = AutomatedPayrollService()
    service.run()

# try:
#     run_payroll_service(repeat=Task.DAILY)
# except:
#     # TODO handle exceptions better
#     pass
