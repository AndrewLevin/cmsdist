### RPM cms batchmanager 1.0.6

Source0: git://github.com/AndrewLevin/relval_batch_assigner.git?obj=master/%{realversion}&export=%n-%{realversion}&output=/%n-%{realversion}.tar.gz
Requires: cherrypy rotatelogs py2-mysqldb

%prep
%setup -b 0 -n %n-%{realversion}

%build

%install
mkdir -p %i/{bin,lib} %i/$PYTHON_LIB_SITE_PACKAGES
cp -pf %_builddir/%n-%{realversion}/* %i/bin/

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
rm -rf %i/etc/profile.d
mkdir -p %i/etc/profile.d
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$?$root = X1 || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done


%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
