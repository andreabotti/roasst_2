from ggplot import *
import pandas as pd



data = pd.read_csv('dat1.csv')
print(data)
g = ggplot(aes(x='Country', y='percent'), data=data) + geom_line() +\
    stat_smooth(colour='blue', span=0.2)


# g = ggplot(dat1,
#     aes(x = Country, y = percent, colour = "red") ) + theme_bw() +\
#         geom_point(size = 4) +\
#         geom_text(
#             aes(label = percent(round(percent/100, 2))), size = 4, hjust = 0.4, vjust = -1, colour = "red") +\
#         geom_bar(aes(y = AppLaunches), stat = 'identity', colour = "blue", alpha = 0.3)+\
#         theme(legend.position='none', axis.text.x=element_text(angle=90,hjust=1,vjust=0.5))  +\
#         labs(x = 'Country', y = 'App Launches') +\
#         ggtitle("Bar Chart")
