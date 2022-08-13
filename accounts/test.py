# str1="I AM GooD"
# import string
# str1=str(input('Enter your string'))
# list1=str1.split(" ")
# result=''
# for i in list1:
#     if len(i)>1:
#         temp=i.lower()
#         result1=temp[0].upper()+temp[1:len(temp)-1]+temp[len(temp)-1].upper()
#     else:
#         result1=temp=i.upper()
#     result=result+' '+result1
# print(result)



    # categories = Categories.objects.filter(job_post_category__gt=0).annotate(
    #     num_job_post=Count('job_post_category')).order_by('-num_job_post')
    
    # district = Job_post.objects.all().annotate(handle_lower=Lower("state")).distinct("handle_lower")
from typing import Counter


list2 =  [4,2,3,1,1,2,4,2,2,8]

list1=[2,4,5,7,8,5,1,0,3,10]

for i in list1:
    for j in list1:
        if i+j==7:
            print(i,j)





print('######################################################################################')

def count(list2):
    # print(a,31)
    for j in list2:
        count=1 
        for i in list2:
            if i==j:
                count=count+1;
                # print(count,36)
                print(j,count)        
    return count        

result= count(list1)
print(result)


from rest_framework import views

urls_pattern=[
    path('delete/<int:pk>',myAPi.as_views())
]


class Father(models.Model):
    child=models.onetomanyfield(child,on_delete=models.PROTECT,related_name='child')


class child(models.Model):
    pass



class myAPi(views.APIView):
    def delete(self,request,pk):
        id=request.get(')
        Father=Father.objects.get(id=pk)


