import math
import numpy as np
import random
import matplotlib
import matplotlib.pyplot as plt
import sys
import os
# bar chart, pie chart, scatter plot, histogram
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# ref: graph_file.py
# color = 'blue'
color_set = ['black', 'red', 'blue', 'green', 'yellow', 'white',\
          'cyan', 'silver', 'orange', 'violet', 'purple', 'brown']
# family='serif'
family_set = ['serif', 'sans-serif', 'cursive', 'fantasy', 'monospace']
# fontname = 'Arial'
fontname_set = ['Sans', 'Courier New', 'Arial', 'Times New Roman', 'Comic Sans MS', \
            'Georgia', 'Calibri', 'Simsun']
fontstyle_set = ['normal', 'italic', 'oblique']
ha_set = ['left', 'right', 'center']
va_set = ['center', 'top', 'bottom', 'baseline']
weight_set = [ 'normal', 'bold' ,'heavy' , 'light' , 'ultrabold', 'ultralight']
linestyle_set = ['dotted', 'dashed', 'solid'] #[':', '--', '-']
                 
def barChart01():
    year = np.arange(10)
    totalSales = np.array([(-num**2+10*num) for num in year])
    width = 0.5
    # print year, totalSales
    fig = plt.figure(figsize=[8,8])
    ax = plt.gca() # axis variable
    yearString = [str(2010+num) for num in year]
    barChart = ax.bar(year, totalSales, width,
                       align='center',
                       color='red',
                       edgecolor='green',
                       linewidth = 2,
                       label ='no of years')
    ax.set_title('Total Sales (y) in Year(x)', fontname='Arial')
    ax.set_xlabel('year', size=15, color='blue')
    ax.set_xticks(year)
    ax.set_xticklabels([('yr'+str(num)) for num in year],
                       size=15, color='blue')
    ax.set_ylabel('total sales', size=15, color='purple', fontname='Courier New')
    yTicks01 = [0, 5, 10, 15, 20, 25, 30]
    ax.set_yticks(yTicks01)
    ax.set_yticklabels(['$%d'%num for num in yTicks01], \
                       size=15, fontname='Courier New', color='purple')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 30)
    ax.grid(True)
    plt.show()
    #fig.savefig('myBarChart01.png', dpi=500, facecolor='yellow', edgecolor='orange',
    #        orientation='landscape', transparent=False, bbox_inches = 'tight',
    #        format='png', pad_inches=0.1, frameon=True)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def barChart02():
    fig = plt.figure(figsize=[7,5], facecolor='silver')
    ax = fig.add_subplot(121) # total number of plots = 1 x 2; this plot = 2nd position
    ind = np.arange(5)
    data01 = [1, 3, 5, 3, 1]
    data02 = [2, 1, 4, 6, 1]
    data03 = [1, 1, 1, 1, 1]
    data04 = [1, 2, 6, 1, 4]
    width = 0.35
    data01_bar = ax.bar(ind-width, data01, width, color='red',  align='edge')
    data02_bar =  ax.bar(ind, data02, width, color='blue',  align='edge')
    data03_bar =  ax.bar(ind-width, data03, width, bottom=data01, color='orange',  align='edge')
    data04_bar =  ax.bar(ind, data04, width, bottom=data02, color='cyan',  align='edge')
    ax.set_title('vertical plot', family='sans-serif', ha='center', va='baseline')
    ax.set_xticks(ind)
    xTickLabel01 = [str(int(num+1))+",000" for num in ind]
    ax.set_xticklabels(xTickLabel01, size=10, rotation=45)
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 10)

    height = 0.2
    ax2 = fig.add_subplot(122)
    data01_barh = ax2.barh(ind-width, data01, height, color='red',  align='edge')
    data02_barh =  ax2.barh(ind, data02,  height, color='blue',  align='edge')
    data03_barh =  ax2.barh(ind-width, data03,  height, left=data01, color='orange',  align='edge')
    data04_barh =  ax2.barh(ind, data04,  height, left=data02, color='cyan',  align='edge')
    ax2.set_title('horizontal plot', family='monospace', ha='center', va='baseline',  color='white',\
                  backgroundcolor='brown')
    ax2.set_ylabel('number', size=15, rotation = 90, va='top')
    plt.show()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def histogram01():
    fig = plt.figure()
    ax = plt.gca()
    #normal distribution
    #mean=0, std deviation=1, sample size = 1000
    x = np.random.normal(0,1,1000)
    xBins = np.arange(-5, 5.1, 0.1)
    bin_size = 100
    ax.hist(x, bins=xBins, histtype='bar', align='mid', \
            orientation='vertical', color='blue', edgecolor='yellow', alpha=0.75)
    #ax.hist(x, bin_size, histtype='bar')

    ax.set_title(r'Normal distribution: $\mu=0$, $\sigma=1$, $S=1,000$',\
                 size=20, fontname='Courier New')
    ax.set_xlabel('x', size=20, fontname='Courier New')
    ax.set_xticks(np.arange(-5, 6, 1))
    ax.set_xticklabels(np.arange(-5, 6, 1), size=15, fontname='Courier New')
    ax.set_ylabel('frequency', size=20, fontname='Courier New', rotation=90)
    ax.set_yticks(np.arange(0, 60, 10))
    ax.set_yticklabels(np.arange(0, 60, 10), size=15, fontname='Courier New')
    ax.set_xlim(-5, 5)
    ax.set_ylim(0, 55)
    ax.grid(True)
    plt.show()
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def histogram02():
    # binomial distribution B(n,p)
    # mu = np = 5, sigma = (np(1-p))^(1/2) = 1.581
    x = np.random.binomial(n=10, p=0.5, size=500) #x.shape=(100,)
    x0 = float(sum(x))/500
    sigma = pow(10*0.5*(1-0.5), 0.5)
    print x0
    myBins = np.arange(-0.5, 10.5, 1)
    histArr, binsArr = np.histogram(x, bins=myBins) #default, number of bars = 10
    # make graph
    fig = plt.figure(figsize=[5,5])
    ax = plt.gca()
    ax.hist(x, bins=myBins, histtype='stepfilled', color='orange', alpha=0.75)
    ax.axvline(x0, color='cyan', linestyle='--')
    ax.axvline(x0+sigma, color='violet', linestyle='--')
    ax.axvline(x0-sigma, color='violet', linestyle='--')
    xMarks = np.zeros(len(binsArr)-1)
    yMarks = np.zeros(len(binsArr)-1)
    for j in range(0, len(binsArr)-1):
        xMarks[j] = (binsArr[j]+binsArr[j+1])/2
    ax.plot(xMarks, histArr, linewidth=1, linestyle='dotted')
    ax.set_title(r'$B(n=10, p=0.5)$',\
                 size=20, fontname='monospace', weight='bold')
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(0,150)
    ax.set_xlabel('No of Success', size=20, family ='monospace')
    ax.set_xticks([1,2,3,4,5,6,7,8,9,10])
    ax.set_xticklabels([1,2,3,4,5,6,7,8,9,10], size=15, family='monospace')
    ax.set_ylabel('Frequency', size=20, family ='monospace')
    ax.set_yticks([0,20,40,60,80,100,120,140])
    ax.set_yticklabels([0,20,40,60,80,100,120,140], size=15, family='monospace')
    ax.grid(True)
    plt.show()
   # fig.savefig('myHistogram02.png', dpi=500, facecolor='none', edgecolor='none',
   #        orientation='landscape', transparent=True, bbox_inches = 'tight',
   #         format='png', pad_inches=0.1, frameon=True)
    return x, histArr, binsArr
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def pieChart01():
    fig = plt.figure()
    ax = plt.gca()
    ax.set_title('Computer languages & Popularity', fontsize=25)
    program_language = ['Python', 'Java', 'Javascript', 'C#', 'PHP', \
                        'C/C++', 'R', 'MATLAB', 'Other']
    popularity = np.array([31, 18, 8, 7, 6, 6, 4, 2, 18])
    explode01 = (0.1, 0, 0, 0, 0, 0, 0, 0, 0)
    colour = ['skyblue', 'gold', 'pink', 'lime', 'orange', 'violet', 'aqua', 'bisque', 'silver']

    myStyle= {'fontsize':20, 'fontname': 'Times New Roman'}
    wedges, labels, autopact = ax.pie(popularity, explode=explode01, labels=program_language,\
                                      colors=colour, autopct='%0.2f%%', shadow=False, startangle=90,\
                                      textprops=myStyle, radius=2)
    ax.legend(wedges, program_language, loc='upper right', ncol=1, fontsize=15, \
              labelspacing = 0.75)
    for lab in labels:
        lab.set_fontsize(20)
    ax.axis('equal')
    plt.show()
    fig.savefig('myPieChart01.png', dpi=500, transparent=True, bbox_inches='tight', \
                format='png', orientation = 'landscape')

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def scatter01():
    fig = plt.figure(figsize=[5,5], facecolor='black')
    ax = fig.add_subplot(111, axisbg = 'black')
    ax.set_title('Scatter in Dark', color='cyan', fontsize=25)
    ax.spines['bottom'].set_color('gold')
    ax.spines['top'].set_color('gold')
    ax.spines['left'].set_color('gold')
    ax.spines['right'].set_color('gold')
    ax.xaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='y', colors='white')
    xyticklabel = [ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() \
                  +  ax.get_yticklabels()
    for item in xyticklabel:
        item.set_fontsize(20)
    N = 1000
    x = np.random.randn(N)
    y = np.random.randn(N)
    sizeArr = np.zeros(N)
    for k in range(0,N):
        sizeArr[k] = int(100*(x[k]**2+y[k]**2))
    ax.scatter(x, y, s=sizeArr, color='blue', alpha=0.5, marker='o', \
              edgecolor='pink', linewidth=1)
    ax.set_aspect(1./ax.get_data_ratio())
    ax.grid(True)
    #ax2 = fig.add_subplot(122)
    #myStyle = {'alpha':0.5, 'edgecolor':'none' }
    plt.show()
    fig.savefig('myScatter01.png', dpi=200, facecolor='black', edgecolor='none',\
                orientation='landscape', transparent=False,  format='png', pad_inches=0.1)






# # # # # # # # # # # # # # # # # # # # MAIN # # # # # # # # # # # # # # # # # # # #
# x, histArr, binsArr = histogram02()

scatter01()


















