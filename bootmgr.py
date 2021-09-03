from util import run_app


class Bootmgr:
    items = {}
    curr_boot_index = ''
    timeout = -1
    orders = []

    def __init__(self):
        self.init()

    def init(self):
        return run_app('efibootmgr', log_function=self.parse_efibootmgr)

    def valid(self) -> bool:
        return len(self.orders) > 0

    def get_boot_item(self, index) -> dict:
        return self.items[index]

    def get_boot_orders(self) -> list:
        return self.orders

    def get_curr_boot_index(self) -> str:
        return self.curr_boot_index

    def get_timeout(self) -> int:
        return self.timeout

    def parse_efibootmgr(self, txt: str):
        if txt.startswith('BootCurrent:'):
            self.curr_boot_index = txt.split()[1]
        elif txt.startswith('Timeout:'):
            self.timeout = int(txt.split()[1])
        elif txt.startswith('BootOrder:'):
            orders = txt.split()[1]
            self.orders = orders.split(',')
        elif txt.startswith('Boot'):
            items = txt.split()
            index = items[0]
            name = txt.replace(index, '').strip()
            index = index.replace('Boot', '')
            index = index.replace('*', '')
            self.items[index] = {
                'name': name
            }

    def set_next_boot(self, index: str):
        if index not in self.items.keys():
            return -1
        err = run_app('efibootmgr -n {}'.format(index), log_function=print)
        if err != 0:
            return err
        return self.init()

    def delete_item(self, index: str):
        if index not in self.items.keys():
            return -1
        err = run_app('efibootmgr -b {} -B'.format(index), log_function=print)
        if err != 0:
            return err
        return self.init()

    def set_boot_orders(self, orders: list):
        txt = ','.join(orders)
        for item in orders:
            if item not in self.items.keys():
                return -1
        curr = ','.join(self.orders)
        if curr == txt:
            return 0
        err = run_app('efibootmgr -o {}'.format(txt), log_function=print)
        if err != 0:
            return err
        return self.init()

