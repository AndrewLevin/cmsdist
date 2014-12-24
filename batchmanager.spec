### RPM cms batchmanager 1.0.0

Source: git://github.com/AndrewLevin/relval_batch_assigner.git?obj=master/%{realversion}&export=%n-%{realversion}&output=/%n-%{realversion}.tar.gz

%prep

%build

touch newfile.txt
echo blah >> newfile.txt

# tar -xvf batchmanager.tar.gz

%install

touch newfile2.txt
echo blah >> newfile2.txt

%post
