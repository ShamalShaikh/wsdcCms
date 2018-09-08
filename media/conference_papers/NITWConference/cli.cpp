#include<bits/stdc++.h>
#include<unistd.h>
#include<fcntl.h>
#include<sys/types.h>
#include<sys/stat.h>
using namespace std;
int main()
{
	string s;
	char *a[10],*k,b[100];
	int i=0,pid,x;
	getline(cin,s,'\n');

	while(s!="exit")
	{
		pid=fork();
		if(pid==-1)
		{
			cout<<"error occured\n";
			exit(-1);
		}
		if(pid==0)
		{
			i=0;
			strcpy(b,s.c_str());
			k=strtok(b," ");
			while(k!=NULL)
			{
				a[i++]=k;
				k=strtok(NULL," ");
			}
			a[i]=NULL;
			
			for(int j=0;j<i;j++)
			{
				if(a[j][0]=='>')
				{
					x=open(a[j+1],O_RDWR | O_CREAT , S_IRWXU);
					dup2(x,1);
					a[j]=NULL; j++;
				}
				if(a[j][0]=='<')
				{
					x=open(a[j+1],O_RDWR , S_IRWXU);
					dup2(x,0);
					a[j]=NULL; j++;
				}
			}

			execvp(a[0],a);
			exit(0);
		}
		if(pid>0)
		{
			wait();
			getline(cin,s,'\n');
		}
	}

	return 0;
}