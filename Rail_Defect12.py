import cv2
import numpy as np
import PySimpleGUI as sg        # интерфейс
import Find_threshold_brown2 as ft     # самописный
import os       #для извлечения имени файла из пути
import Add_spot2 as ast     # Для добавления области
import random
import json

# -*- coding: utf-8 -*-

point1 = None
point2 = None
frame_start = None
frame_end = None
image_mini = None
dark_spots = []
etalon_line = 100
names = []
dark_spots_dict = {}
sum=0
ipass = 0
len_def_sum = 0     # variable for summary defects length
no_defects=False


def calculate_distance(p1, p2):
    return (p2[0] - p1[0]) 

def read_ini_file(filename):
    path=''
    try:
        f = open(filename, mode='rt')
        path = f.read()
        f.close()
    except FileNotFoundError:
        sg.popup_error_with_traceback('Файл result.ini не найден')
    return (path)

def read_json_file(filename):
    foldername_path = filename
    with open(foldername_path) as f:
        folder_name = json.load(f)
        print (f"название директории {folder_name} подгружено в основной программе")
    return (folder_name)


   
try:
    threshold_value, image_mini, dark_spots, frame_start, frame_end, point1, point2, file_path, LH, LS, LV, UH, US, UV, pixel_per_cm = ft.main()
except:
    pass

key = cv2.waitKey(0)

#dark_spots = on_key(key)
if dark_spots:

    #формируем словарь   ///этот кусок кода для отображения окошка со списком найденных дефектов
    numbers = list(range(0, len(dark_spots)))
    dark_spots_dict =dict(zip(numbers, dark_spots))

    for i in range(len(dark_spots_dict)):
        names.append(str(i))
    layout_lst = [[sg.Text('Rail',size=(20, 1), font='Lucida',justification='left')],
                    [sg.Listbox(names, select_mode='single', key='list1', size=(30, 6))],
                    [sg.Button('Remove', font=('Times New Roman', 12)), sg.Button('Add', font=('Times New Roman', 12)), sg.Button('Cancel', font=('Times New Roman',12)), 
                     sg.Button('Back', font=('Times New Roman',12)), sg.Button('Next', font=('Times New Roman',12)), sg.Button('No_defects', font=('Times New Roman',12)), sg.Button('Calculate', font=('Times New Roman',12))]]
    window_list=sg.Window('Defects', layout_lst)

    ttemp_image = image_mini.copy()
    for dark_spot in dark_spots:
        (x, y, w, h, dimensions) = dark_spot
        cv2.rectangle(ttemp_image, (x + frame_start[0], y + frame_start[1]), (x + frame_start[0] + w, y + frame_start[1] + h), (0, 255, 0), 2)
    file_name= os.path.basename(file_path)
    firststep = True
    while True:
        if key == ord("q"):
            break
        sum=0
        e,v=window_list.read()

        temp_list=list(dark_spots_dict.keys())
        try:
            v['list1']=str(temp_list[int(ipass)])
        except:
            v['list1']=str(random.choice(temp_list))
        print(e, v, ' ipass > ', ipass)

        if e == 'Remove':
            if len(dark_spots_dict)>1:
                names.remove(v['list1'])
                dark_spots_dict.pop(int(v['list1']))
                window_list['list1'].update(names)
                temp_list=list(dark_spots_dict.keys())
                temp2_image = image_mini.copy()
                for new_spot_list in dark_spots_dict:
                    (x, y, w, h, dimensions) = dark_spots_dict[new_spot_list]
                    cv2.rectangle(temp2_image, (x + frame_start[0], y + frame_start[1]), (x + frame_start[0] + w, y + frame_start[1] + h), (235, 0, 255), 2)
                if ipass>=1:
                    ipass-=1
                else:
                    ipass=len(dark_spots_dict)-1
            else:
                pass
        elif e == 'Add':
            no_defects=False
            try:
                max_num = [max(dark_spots_dict.items(), key=lambda k_v: k_v[0])][0][0]
                test, x_add, y_add, contour_add = ast.main('Identified defects', temp2_image, pixel_per_cm, LH, LS, LV, UH, US, UV)
                dark_spots_dict[max_num+1] = (test[0]+x_add-frame_start[0], test[1]+y_add-frame_start[1], test[2], test[3], test[4])
                
                for new_spot_list in dark_spots_dict:
                    (x, y, w, h, dimensions) = dark_spots_dict[new_spot_list]
                    cv2.rectangle(temp2_image, (x + frame_start[0], y + frame_start[1]), (x + frame_start[0] + w, y + frame_start[1] + h), (235, 0, 255), 2)
            except:
                sg.popup_auto_close('Либо нет дефектов в окне, либо dark_spot_dict пустой ')
                pass
        elif e == 'Cancel':
            window_list.close()
            break
        elif e == 'Next':
            if ipass<len(dark_spots_dict)-1:
                ipass+=1
            else:
                ipass=0
            temp_list=list(dark_spots_dict.keys())
            v['list1']=str(temp_list[ipass])
        elif e == 'Back':
            if ipass>=1:
                ipass-=1
            else:
                ipass=len(dark_spots_dict)-1
            temp_list=list(dark_spots_dict.keys())
            v['list1']=str(temp_list[ipass])
        elif e == 'No_defects':
            no_defects=True
        elif e == 'Calculate':
            if no_defects:
                try:
                    cv2.putText(temp2_image, f"Summary Square: 0 cm^2", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (235, 0, 255), 3)
                    cv2.putText(temp2_image, 'Number of defects: 0 pcs', (100, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (235, 0, 255), 2)
                except:
                    temp2_image = image_mini.copy()
                    cv2.putText(temp2_image, f"Summary Square: 0 cm^2", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (235, 0, 255), 2)
                    cv2.putText(temp2_image, 'Number of defects: 0 pcs', (100, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (235, 0, 255), 2)
                
                destination_path = read_json_file('folder.json')
                my_txt_file_name = file_name.replace('.jpg', '.txt')
                my_txt_file = open(destination_path + my_txt_file_name, "w+")
                my_txt_file.write('Имя файла ' + '\t' + ' Обнаружено дефектов ' + '\t' + ' Общая площадь дефектов,кв.см. ' + '\t' + ' Средняя площадь дефекта,кв.см. '+ '\t' + 'Общая длина дефектов' + '\t' + ' Настройки HSV нижние - HSV верхние ' + '\n')
                my_txt_file.write(my_txt_file_name + '\t' + '0' + '\t' + '0' + "\t" + '0' + "\t" + '0' + "\t"
                                  + ' ' + str(LH) + ' ' + str(LS) + ' ' + str(LV) + ' ' + str(UH) + ' ' + str(US) + ' ' + str(UV)+ '\n')
                my_txt_file.close()
                # save image with rectangles
                my_jpg_file_name = '_'+file_name
                isWritten = cv2.imwrite(destination_path + my_jpg_file_name, temp2_image)
                if isWritten: print('Image is successfully saved as _'+ my_jpg_file_name+' *.jpg file.')
                len_def_sum = 0

            else:
                for i in dark_spots_dict:
                    sum += dark_spots_dict[i][4]
                try:
                    cv2.putText(temp2_image, f"Summary Square: {sum:.3f} cm^2", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (235, 0, 255), 3)
                    cv2.putText(temp2_image, 'Number of defects: '+ str(len(dark_spots_dict)) + ' pcs', (100, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (235, 0, 255), 2)
                except:
                    temp2_image = image_mini.copy()
                    for new_spot_list in dark_spots_dict:
                        (x, y, w, h, dimensions) = dark_spots_dict[new_spot_list]
                        cv2.rectangle(temp2_image, (x + frame_start[0], y + frame_start[1]), (x + frame_start[0] + w, y + frame_start[1] + h), (235, 0, 255), 2)
                    cv2.putText(temp2_image, f"Summary Square: {sum:.3f} cm^2", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (235, 0, 255), 2)
                    cv2.putText(temp2_image, 'Number of defects: '+ str(len(dark_spots_dict)) + ' pcs', (100, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (235, 0, 255), 2)
                # calculate summary defects length
                for j in dark_spots_dict:
                    len_def_sum += dark_spots_dict[j][2]/(calculate_distance(point1, point2)/etalon_line)
                # save text table
                destination_path = read_json_file('folder.json')
                #destination_path = read_ini_file('result.ini')
                my_txt_file_name = file_name.replace('.jpg', '.txt')
                my_txt_file = open(destination_path + my_txt_file_name, "w+")
                my_txt_file.write('Имя файла ' + '\t' + ' Обнаружено дефектов ' + '\t' + ' Общая площадь дефектов,кв.см. ' + '\t' + ' Средняя площадь дефекта,кв.см. '+ '\t' + 'Общая длина дефектов' + '\t' + ' Настройки HSV нижние - HSV верхние ' + '\n')
                my_txt_file.write(my_txt_file_name + '\t' + str(len(dark_spots_dict)) + '\t' + str("{:.2f}".format(sum)) + "\t" + str("{:.2f}".format(sum/len(dark_spots_dict))) + "\t" + str("{:.2f}".format(len_def_sum)) + "\t"
                                  + ' ' + str(LH) + ' ' + str(LS) + ' ' + str(LV) + ' ' + str(UH) + ' ' + str(US) + ' ' + str(UV)+ '\n')
                my_txt_file.write('Номер дефекта' + '\t' + 'Длина' + '\t' + 'Ширина' + '\t' + 'Площадь' + '\n')
                for j in dark_spots_dict:
                    my_txt_file.write(str(j) + '\t' + str("{:.2f}".format(dark_spots_dict[j][2]/(calculate_distance(point1, point2)/etalon_line))) + '\t' + str("{:.2f}".format(dark_spots_dict[j][3]/(calculate_distance(point1, point2)/etalon_line))) + '\t' + str("{:.2f}".format(dark_spots_dict[j][4])) + '\n')
                my_txt_file.close()
                # save image with rectangles
                my_jpg_file_name = '_'+file_name
                isWritten = cv2.imwrite(destination_path + my_jpg_file_name, temp2_image)
                if isWritten: print('Image is successfully saved as _'+ my_jpg_file_name+' *.jpg file.')
                len_def_sum = 0

        #  /// окончание куска кода для  отображения окошка со списком найденных дефектов
        temp_list=list(dark_spots_dict.keys())
        try:
            v['list1']=str(temp_list[ipass])
        except:
            v['list1']=str(random.choice(temp_list))
        (x, y, w, h, dimensions) = dark_spots_dict[int(v['list1'])]

        result_image = ttemp_image.copy()
        cv2.rectangle(result_image, (x + frame_start[0], y + frame_start[1]), (x + frame_start[0] + w, y + frame_start[1] + h), (0, 0, 255), 2)
        
        # Add dimensions text to the dark spot
        width_cm = w / (calculate_distance(point1, point2)/etalon_line)
        height_cm = h / (calculate_distance(point1, point2)/etalon_line)
        cv2.putText(result_image, f"Square: {dimensions:.3f} cm^2", (x + frame_start[0], y + frame_start[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        cv2.putText(result_image, f"Width: {width_cm:.3f} cm", (x + frame_start[0], y + frame_start[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        cv2.putText(result_image, f"Height: {height_cm:.3f} cm", (x + frame_start[0], y + frame_start[1] + h + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        cv2.imshow("Identified defects", result_image)
        try:
            cv2.imshow("Result", temp2_image)
        except: pass

cv2.destroyAllWindows()


