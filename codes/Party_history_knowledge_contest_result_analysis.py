import xlrd
import xlsxwriter
import time

# 南京大学软件学院党史知识竞赛成绩统计程序
def insert(result: dict, classname: str, sid: str, grade: int, id : int, commit_time : str, time : int, name:str):
    if sid in result[classname]["sid_list"]: #多次提交
        index = result[classname]["sid_list"].index(sid)
        result[classname]["participant_num"] += 1
        result[classname]["commit_number"][index] += 1
        if grade > result[classname]["grade_list"][index]:
            result[classname]["total_grade"] += (grade - result[classname]["grade_list"][index])
            result[classname]["grade_list"][index] = grade
            result[classname]["time_list"][index] = time
            result[classname]["commit_id"][index] = id
            result[classname]["commit_time"][index] = commit_time
        elif grade == result[classname]["grade_list"][index]:
            if time <= result[classname]["time_list"][index]:
                result[classname]["time_list"][index] = time
                result[classname]["commit_id"][index] = id
                result[classname]["commit_time"][index] = commit_time
    # 第一次提交
    else:
        result[classname]["sid_list"].append(sid)
        result[classname]["grade_list"].append(grade)
        result[classname]["total_grade"] += grade
        result[classname]["time_list"].append(time)
        result[classname]["name_list"].append(name)
        result[classname]["commit_id"].append(id)
        result[classname]["commit_time"].append(commit_time)
        result[classname]["commit_number"].append(1)
        result[classname]["participant_num"] += 1
        result[classname]["effective_num"] += 1


def count(result: dict):
    print("--------------------开始统计--------------------")
    # 统计
    # todo
    workbook = xlrd.open_workbook("./data/116921481_1_南京大学软件学院 quot重温百年党史  汲取成长力量quot 党史知识竞赛初赛_862_845.xlsx")
    sheet = workbook.sheet_by_index(0)
    total_rows = sheet.nrows - 1
    for i in range(1, total_rows + 1):
        row_vlues = sheet.row_values(rowx=i, start_colx=0, end_colx=13)
        if type(row_vlues[9]) == float:
            row_vlues[9] = str(int(row_vlues[9]))
        # print(row_vlues)
        if row_vlues[10] == "其他":
            insert(result, row_vlues[10], row_vlues[9], int(row_vlues[7]), row_vlues[0], row_vlues[2], int(row_vlues[3][0:-1]), row_vlues[5])
        elif row_vlues[10][0] == "大":
            insert(result, row_vlues[10] + row_vlues[12], row_vlues[9], int(row_vlues[7]), row_vlues[0], row_vlues[2], int(row_vlues[3][0:-1]), row_vlues[5])
        elif row_vlues[10][0] == "研":
            insert(result, row_vlues[10] + row_vlues[11], row_vlues[9], int(row_vlues[7]), row_vlues[0], row_vlues[2], int(row_vlues[3][0:-1]), row_vlues[5])
    print("--------------------统计完成--------------------")
    return result



def init():
    # 初始化
    print("--------------------开始初始化--------------------")
    example_workbook = xlrd.open_workbook("./data/结果统计.xlsx")
    example_sheet = example_workbook.sheet_by_index(0)
    result = {}
    for i in range(1, 39):
        row_vlues = example_sheet.row_values(rowx=i, start_colx=0, end_colx=4)
        temp = {}
        temp["classid"] = int(row_vlues[0])
        temp["classname"] = row_vlues[1]
        temp["participant_num"] = 0
        temp["total_grade"] = 0
        temp["effective_num"] = 0
        temp["grade_list"] = []
        temp["sid_list"] = []
        temp["name_list"] = []
        temp["time_list"] = []
        temp["commit_id"] = []
        temp["commit_time"] = []
        temp["commit_number"] = []
        result[row_vlues[1]] = temp
    print("--------------------已完成初始化--------------------")
    return result


def save(result: dict):
    #存储数据
    print("--------------------开始存储数据--------------------")
    time_stamp = time.strftime("%Y年%m月%d日 %H时%M分%S秒", time.localtime())
    workbook = xlsxwriter.Workbook('党史知识竞赛结果统计' + time_stamp + '.xlsx')
    sheet1 = workbook.add_worksheet("统计")
    sheet3 = workbook.add_worksheet("去重汇总")
    # sheet4 = workbook.add_worksheet("所有记录")
    header = ['软件学院党史知识竞赛结果统计  ' + time_stamp]
    headings = ['序号', '支部', '参与人次', '有效人数', '平均成绩']
    sheet1.write_row('A1', header)
    sheet1.write_row('A2', headings)
    header3 = ["所有参赛同学成绩汇总" + time_stamp]
    headings3 = ["学号","姓名", "最高成绩", "提交id", "提交时间", "用时", "提交次数"]
    sheet3.write_row('A1', header3)
    sheet3.write_row('A2', headings3)
    sheet3.set_column("A:A", 10)
    sheet3.set_column("B:D", 8)
    sheet3.set_column("E:E", 19)
    sheet3.set_column("F:G", 8)

    row_index = 3
    index = 3
    for i in result:
        if result[i]["effective_num"] == 0:
            average = "0"
        else:
            average = "{:.4f}".format(result[i]["total_grade"]/result[i]["effective_num"])
            sheet2 = workbook.add_worksheet(result[i]["classname"])
            sheader = [result[i]["classname"] + "成绩统计"]
            sheadings = headings3
            sheet2.write_row("A1", sheader)
            sheet2.write_row("A2", sheadings)
            sheet2.set_column("A:A", 10)
            sheet2.set_column("B:D", 8)
            sheet2.set_column("E:E", 19)
            sheet2.set_column("F:G", 8)
            sheet2.write_column('A3', result[i]["sid_list"])
            sheet2.write_column('B3', result[i]["name_list"])
            sheet2.write_column('C3', result[i]["grade_list"])
            sheet2.write_column('D3', result[i]["commit_id"])
            sheet2.write_column('E3', result[i]["commit_time"])
            sheet2.write_column('F3', result[i]["time_list"])
            sheet2.write_column('G3', result[i]["commit_number"])

            sheet3.write_column('A' + str(row_index), result[i]["sid_list"])
            sheet3.write_column('B' + str(row_index), result[i]["name_list"])
            sheet3.write_column('C' + str(row_index), result[i]["grade_list"])
            sheet3.write_column('D' + str(row_index), result[i]["commit_id"])
            sheet3.write_column('E' + str(row_index), result[i]["commit_time"])
            sheet3.write_column('F' + str(row_index), result[i]["time_list"])
            sheet3.write_column('G' + str(row_index), result[i]["commit_number"])
            row_index += len(result[i]["sid_list"])
        temp = [result[i]["classid"], result[i]["classname"], result[i]["participant_num"], result[i]["effective_num"], average]
        sheet1.write_row('A'+str(index), temp)
        index += 1
        # print("--------------------" + result[i]["classname"] + "数据已处理完成--------------------")
    workbook.close()
    print("--------------------存储数据完成--------------------")


def start():
    result = init()
    result = count(result)
    save(result)


if __name__ == "__main__":
    start()
