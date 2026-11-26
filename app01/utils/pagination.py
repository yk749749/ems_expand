# app01/utils/pagination.py
from django.utils.safestring import mark_safe


class Pagination(object):
    def __init__(self, request, queryset, page_size=10, page_param="page", plus=5):
        """
        :param request: 请求对象，用于获取当前URL中的参数
        :param queryset: 要分页的数据（如 models.PrettyNum.objects.all()）
        :param page_size: 每页显示多少条数据
        :param page_param: URL中传递页码的参数名，默认是 "page"
        :param plus: 当前页前后显示几个页码（如当前第5页，显示1-9页）
        """
        import copy
        query_dict = copy.deepcopy(request.GET)   # 必须深拷贝，否则会修改原请求
        query_dict._mutable = True                # 允许修改
        self.query_dict = query_dict
        self.page_param = page_param

        # 1. 获取当前页码
        page = request.GET.get(page_param, "1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = page_size

        # 2. 计算起始和结束位置
        self.start = (page - 1) * page_size
        self.end = page * page_size

        # 3. 切片获取当前页的数据
        self.page_queryset = queryset[self.start:self.end]

        # 4. 计算总页数
        total_count = queryset.count()
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count
        self.plus = plus

    def _jump_html(self):
        """生成【跳转到指定页码】的 HTML + JS"""
        total = self.total_page_count
        param = self.page_param

        jump = (
            '<li class="pagination-jump" style="display:inline-flex;align-items:center;margin-left:8px;">'
            f'<input type="number" class="form-control input-sm" '
            f'min="1" max="{total}" '
            'placeholder="页码" '
            'style="width:70px;height:34px;text-align:center;display:inline-block;'
            'border-radius:4px 0 0 4px;" '
            "onkeydown=\"if (event.key === 'Enter') { this.nextElementSibling.click(); }\">"
            f'<button type="button" class="btn btn-default btn-sm" '
            f'data-total="{total}" data-param="{param}" '
            'onclick="window.pageJump(this)" '
            'style="height:34px;border-radius:0 4px 4px 0;margin-left:-1px;">跳转</button>'
            '</li>'
        )

        # 只定义一次（页面存在多个分页组件时不会重复定义）
        script = (
            '<script>'
            'window.pageJump = window.pageJump || function (btn) {'
            '    var input = btn.previousElementSibling;'
            '    var total = parseInt(btn.getAttribute("data-total"), 10) || 1;'
            '    var param = btn.getAttribute("data-param") || "page";'
            '    var page  = parseInt(input.value, 10);'
            '    if (isNaN(page)) { page = 1; }'
            '    if (page < 1)     { page = 1; }'
            '    if (page > total) { page = total; }'
            '    var url = new URL(window.location.href);'
            '    url.searchParams.set(param, page);'   # // 自动替换/追加 page 参数，保留其它参数
            '    window.location.href = url.toString();'
            '};'
            '</script>'
        )
        return jump + script

    def html(self, always_show=False):
        """生成前端分页的 HTML 代码"""
        # 没有数据时不显示分页
        if self.total_page_count == 0:
            return mark_safe("")
        # 数据太少、不足一页时，默认不需要分页
        # always_show=True 时即使只有一页也显示分页栏（管理员列表使用）
        if self.total_page_count == 1 and not always_show:
            return mark_safe("")

        # 计算显示哪些页码（计算前后plus页的范围）
        if self.total_page_count <= 2 * self.plus + 1:
            start_page = 1
            end_page = self.total_page_count
        else:
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                if (self.page + self.plus) > self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        page_str_list = []

        # 首页
        self.query_dict.setlist(self.page_param, [1])
        page_str_list.append(f'<li><a href="?{self.query_dict.urlencode()}">首页</a></li>')

        # 上一页
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prev = f'<li><a href="?{self.query_dict.urlencode()}">上一页</a></li>'
        else:
            prev = '<li><a href="javascript:void(0);">上一页</a></li>'
        page_str_list.append(prev)

        # 中间页码
        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = f'<li class="active"><a href="?{self.query_dict.urlencode()}">{i}</a></li>'
            else:
                ele = f'<li><a href="?{self.query_dict.urlencode()}">{i}</a></li>'
            page_str_list.append(ele)

        # 下一页
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            next_page = f'<li><a href="?{self.query_dict.urlencode()}">下一页</a></li>'
        else:
            next_page = '<li><a href="javascript:void(0);">下一页</a></li>'
        page_str_list.append(next_page)

        # 尾页
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        page_str_list.append(f'<li><a href="?{self.query_dict.urlencode()}">尾页</a></li>')

        # 跳转
        page_str_list.append(self._jump_html())

        return mark_safe(''.join(page_str_list))