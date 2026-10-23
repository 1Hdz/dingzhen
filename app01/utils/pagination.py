import math
from django.utils.safestring import mark_safe


class Pagination:
    """通用分页组件：自动算页码、切片、保留搜索条件"""

    def __init__(self, request, total_count, per_page=10, max_show=11):
        self.per_page = per_page          # 每页显示条数
        self.max_show = max_show          # 最多显示多少个页码按钮
        self.half_show = max_show // 2    # 当前页左右各显示几个

        self.total_count = total_count
        self.total_page = math.ceil(total_count / per_page)  # 总页数

        # 当前页码（非法值兜底）
        try:
            self.page = int(request.GET.get('page', 1))
        except (ValueError, TypeError):
            self.page = 1
        if self.page < 1:
            self.page = 1
        if self.page > self.total_page:
            self.page = self.total_page

        # 数据库切片区间
        self.start = (self.page - 1) * per_page
        self.end = self.page * per_page

        # 保留原来的搜索参数（q 等），只改 page
        self.query_dict = request.GET.copy()
        self.query_dict._mutable = True

    @property
    def start_index(self):
        return self.start

    @property
    def end_index(self):
        return self.end

    def html(self):
        # 计算要显示的页码区间
        if self.total_page <= self.max_show:
            page_start, page_end = 1, self.total_page
        else:
            if self.page <= self.half_show:
                page_start, page_end = 1, self.max_show
            elif self.page + self.half_show >= self.total_page:
                page_start, page_end = self.total_page - self.max_show + 1, self.total_page
            else:
                page_start, page_end = self.page - self.half_show, self.page + self.half_show

        items = []

        # 首页
        self.query_dict['page'] = 1
        items.append(f'<li><a href="?{self.query_dict.urlencode()}">首页</a></li>')

        # 上一页
        self.query_dict['page'] = self.page - 1
        items.append(f'<li><a href="?{self.query_dict.urlencode()}">上一页</a></li>')

        # 数字页码
        for p in range(page_start, page_end + 1):
            self.query_dict['page'] = p
            url = f'?{self.query_dict.urlencode()}'
            active = ' class="active"' if p == self.page else ''
            items.append(f'<li{active}><a href="{url}">{p}</a></li>')

        # 下一页
        self.query_dict['page'] = self.page + 1
        items.append(f'<li><a href="?{self.query_dict.urlencode()}">下一页</a></li>')

        return mark_safe('<ul class="pagination">' + ''.join(items) + '</ul>')
