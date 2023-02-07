import sys
import numpy as np
import json
from pyecharts.globals import ThemeType
from pyecharts import options as opts
from pyecharts.charts import Bar, Line


def main(args):
    with open('data/sample' + args[0] + '.json', 'r') as f:
        data = json.load(f)

    story_key = []
    story_summary = []
    story_point = []
    story_sprint = []
    story_subtasks = []
    subtasks_key = []
    subtasks_summary = []

    for story_num in data:
        story_key.append(story_num["key"])
        story_summary.append(story_num["fields"]["summary"])
        story_point.append(story_num["fields"]["customfield_10028"])
        cache_story_sprint = []
        for i in story_num["fields"]["customfield_10020"]:
            cache_story_sprint.append(i["name"])
        story_sprint.append(cache_story_sprint)
        for i in story_num["fields"]["subtasks"]:
            story_subtasks.append(i)
        cache_subtasks_key = []
        cache_subtasks_summary = []
        for i in story_num["fields"]["subtasks"]:
            cache_subtasks_key.append(i["key"])
            cache_subtasks_summary.append(i["fields"]["summary"])
        subtasks_key.append(cache_subtasks_key)
        subtasks_summary.append(cache_subtasks_summary)

    for i in np.arange(0, len(story_key)):
        print('sprint_number : ', story_sprint[i])
        print('story_number : ', story_key[i])
        print('story_point : ', story_point[i])
        print('subtask_number : ', subtasks_key[i])
        print('subtask_title : ', subtasks_summary[i])

        print("-------------------------------------------")

    """=====================[bug]==================================="""
    bug_number = []
    for i in np.arange(0, len(data)):
        num = 0
        for p in np.arange(0, len(subtasks_summary[i])):
            if "BUG" in subtasks_summary[i][p]:
                num = num + 1
        bug_number.append(num)

    """=====================[QA]==================================="""
    second_test = []
    for i in np.arange(0, len(data)):
        num = 0

        for p in np.arange(0, len(subtasks_summary[i])):
            if "2nd" in subtasks_summary[i][p]:
                num = num + 1
        second_test.append(num)

    """=====================[visualization]==================================="""
    # x axis : story_key
    # y axis (L) : bug_number
    # y axis (R) : story_point

    # draw a bar chart
    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK))
        .add_xaxis(story_key)
        .add_yaxis("bug_number", bug_number, yaxis_index=0)
        .add_yaxis("2nd_test_execution", second_test, yaxis_index=0)

        #
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Sprint " + args[0], subtitle=''),
            legend_opts=opts.LegendOpts(is_show=True, type_='scroll'),  # 圖例
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            yaxis_opts=opts.AxisOpts(
                name="bug_number",
                position="left",
                axislabel_opts=opts.LabelOpts(formatter="{value}"),
            )
        )

        # 延伸軸
        .extend_axis(
            yaxis=opts.AxisOpts(
                name="story point",
                type_="value",
                position="right",
                axislabel_opts=opts.LabelOpts(formatter="{value}"),
            )
        )
    )

    # 折線圖
    line = (
        Line()
        .add_xaxis(story_key)
        # .add_yaxis('bug_number', bug_number, yaxis_index=1)
        .add_yaxis('story_point', story_point, yaxis_index=1)
    )

    bar.overlap(line)

    print("1")
    bar.render(path="result/sprint" + args[0] + ".html")


if __name__ == '__main__':
    main(sys.argv[1:])
