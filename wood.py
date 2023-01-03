class Wood:
    def __init__(self, build_time, workers, button, res1, res2, res3, level):
        self.build_time = build_time
        self.workers = workers
        self.button = button
        self.res1 = res1
        self.res2 = res2
        self.res3 = res3
        self.level = level

    def request_link(self, session, build):
        # check if the current resources and workers are sufficient
        res1, res2, res3 = self.res1, self.res2, self.res3
        if build.stone_left < res1 or build.wood_left < res2 or build.iron_left < res3 or build.free_workers_left < self.workers:
            print('Not enough resources or workers')
            return

        # make the request to the link
        session.get(self.link)
        print('Building succeffuly upgraded')
        return
