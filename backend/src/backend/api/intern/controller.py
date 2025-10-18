from fastapi_controllers import Controller, get


class InternController(Controller):
    prefix = "/intern"
    tags = ["intern"]

    @get("/")
    async def get_info(self):
        data = [
            {
                "study_program": "институт экологии / 18.03.02 «Энерго- и ресурсосберегающие процессы в химической технологии, нефтехимии и биотехнологии»",
                "start_date": "2025-06-15",
                "end_date": "2025-07-26",
                "students_count": 24,
                "company_reserved": True,
            },
            {
                "study_program": "институт экологии / 05.04.06 «Комплексное управление твердыми бытовыми отходами» (иностранные студенты из Ганы, переводчик у них будет)",
                "start_date": "2025-05-12",
                "end_date": "2025-07-20",
                "students_count": 16,
                "company_reserved": False,
            },
            {
                "study_program": "институт экологии / 05.04.06 «Управление климатическими проектами» (иностранные студенты из Ганы, переводчик у них будет)",
                "start_date": "2025-04-28",
                "end_date": "2025-07-03",
                "students_count": 21,
                "company_reserved": False,
            },
            {
                "study_program": "экономический факультет / «Менеджмент», профиль Маркетинг",
                "start_date": "2025-06-30",
                "end_date": "2025-07-13",
                "students_count": 6,
                "company_reserved": True,
            },
            {
                "study_program": "факультет физико-математических и естественных наук / 02.03.01 Математика и компьютерные науки",
                "start_date": "2025-04-21",
                "end_date": "2025-05-03",
                "students_count": 1,
                "company_reserved": True,
            },
            {
                "study_program": "факультет физико-математических и естественных наук / 01.03.02 Прикладная математика и информатика",
                "start_date": "2025-04-21",
                "end_date": "2025-05-03",
                "students_count": 5,
                "company_reserved": True,
            },
            {
                "study_program": "факультет физико-математических и естественных наук / 02.03.01 Математика и компьютерные науки",
                "start_date": "2025-04-21",
                "end_date": "2025-05-03",
                "students_count": 1,
                "company_reserved": False,
            },
            {
                "study_program": "факультет физико-математических и естественных наук / 01.03.02 Прикладная математика и информатика",
                "start_date": "2025-04-21",
                "end_date": "2025-05-03",
                "students_count": 5,
                "company_reserved": False,
            },
            {
                "study_program": "институт экологии / 18.03.02 «Энерго- и ресурсосберегающие процессы в химической технологии, нефтехимии и биотехнологии» (3 курс, производственная практика)",
                "start_date": "2025-06-23",
                "end_date": "2025-07-20",
                "students_count": 3,
                "company_reserved": True,
            },
            {
                "study_program": "Экология и природопользование (преддипломная практика, 4 курс)",
                "start_date": "2025-06-23",
                "end_date": "2025-07-06",
                "students_count": 1,
                "company_reserved": True,
            },
        ]
        return data