cq <- read.csv("cq2.csv",sep = ",", stringsAsFactors = FALSE)
cq <- cq[, -11]
names(cq) <- c('名字','户型','面积','朝向','装修','电梯','楼层','区域','价格(万元)','单价(平方米)')
# delete the row with NA
cq2data <-na.omit(cq)
head(cq2data)

# delete 别墅 data
bieshuIndex  <- grep("..别墅",cq2data$户型)
cq2data <- cq2data[-bieshuIndex,]

library(ggplot2)

type_tag <- c('3室2厅','4室2厅','2室2厅','1室1厅','2室1厅','1室0厅')
# 重新划分户型(三目运算符) 这里有点问题,先曲线酒国了
hx <- as.character(cq2data$户型)
cq2data$type.new <- ifelse(hx  %in% type_tag, hx , '其他')

type_freq <- data.frame(table(cq2data$type.new))
# 绘图
type_p <- ggplot(data = type_freq, mapping = aes(x = reorder(Var1, -Freq),y = Freq)) + geom_bar(stat = 'identity', fill = 'steelblue') + theme(axis.text.x  = element_text(angle = 30, vjust = 0.5)) + xlab('户型') + ylab('套数')
type_p
