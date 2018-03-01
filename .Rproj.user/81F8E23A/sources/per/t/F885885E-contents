library(ggplot2)
library(scales)
library(gridExtra)
library(reshape2)
library(caTools)
library(pscl)

df <- read.csv('train_data_diff.csv')
df_wins <- subset(df, Result == 1)
df_losses <- subset(df, Result == 0)
df_num <- subset(df, select = -c(Coach) )


#######PPG
###WINS
g1 <-ggplot(aes(x = PPG_Diff, y = Result), data = df_wins) +
  geom_bar(stat = 'identity', width = .75) +
  labs( title = 'PPG_differential to Wins') +
  ylab('Wins') +
  xlab('PPG_Differential') +
  xlim(-35, 35)

###osses
g2 <-ggplot(aes(x = PPG_Diff, y = Result + 1), data = df_losses) +
  geom_bar(stat = 'identity', width = .75) +
  labs( title = 'PPG_differential to Losses') + 
  ylab('Losses') +
  xlab('PPG_Differential') +
  xlim(-35, 35)

grid.arrange(g1, g2, nrow = 2)



##Correlation Matrix and HEAT
cor_matrix <- cor(df_num)
cormat <- round(cor_matrix, 2)
melted_cormat <- melt(cormat)

ggplot(data = melted_cormat, aes(x=Var1, y=Var2, fill=value)) + 
  geom_tile()+
  scale_fill_gradient2(low = "blue", high = "red", 
                       midpoint = 0, limit = c(-1,1), space = "Lab", 
                       name="Pearson\nCorrelation") +
  theme_minimal()+
  coord_fixed()




##USe RSCRIPT TO READ CORRELATIONS IN CMD
cat("PPG: ", cor(df$PPG_Diff, df$Result))
cat("\n")
#FGP
cat("FGP: ",cor(df$FGP_Diff, df$Result))
cat("\n")
#AST
cat("AST: ",cor(df$AST_Diff, df$Result))
cat("\n")
#FGP3
cat("FGP3: ",cor(df$FGP3_Diff, df$Result))
cat("\n")
#FTP
cat("FTP: ",cor(df$FTP_Diff, df$Result))
cat("\n")
#OR
cat("OR: ",cor(df$OR_Diff, df$Result))
cat("\n")
#Dr
cat("DR: ",cor(df$DR_Diff, df$Result))
cat("\n")
#Stl
cat("STL: ",cor(df$STL_Diff, df$Result))
cat("\n")
#Blk
cat("BLK: ",cor(df$BLK_Diff, df$Result))
##FACTORS: FGP-.9, PPG-.85, AST-.79, FGP3-.83, DR-.83, BLK-.49, STL-.48, FTP-.38, OR-.19


#LOG REG
train <- df_num[1:12896,]
test <- df_num[12897:17194,]

model <- glm(Result ~.,family=binomial(link='logit'),data=train)

summary(model)
anova(model, test="Chisq")

pR2(model)

fitted.results <- predict(model,newdata=subset(test,select=c(1,2,3,4,5,6,7,8,9,10,11,12)),type='response')
fitted.results <- ifelse(fitted.results > 0.5,1,0)
misClasificError <- mean(fitted.results != test$Result)

print(paste('Accuracy',1-misClasificError))