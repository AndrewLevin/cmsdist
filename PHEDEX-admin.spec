### RPM cms PHEDEX-admin PHEDEX_4_1_3

## INITENV +PATH PERL5LIB %i/perl_lib
%define downloadn %(echo %n | cut -f1 -d-)
%define gittag 7572e79f0925d593180e1b6a62e2ae1ae29c0f39
Source: git://github.com/dmwm/PHEDEX?obj=master/%gittag&export=%n&output=/%{downloadn}-admin.tar.gz

# Oracle libs
Requires: oracle oracle-env 
# perl libs
Requires: p5-time-hires p5-text-glob p5-compress-zlib p5-dbi
Requires: p5-dbd-oracle p5-xml-parser p5-poe p5-poe-component-child
Requires: p5-log-log4perl p5-log-dispatch p5-log-dispatch-filerotate
Requires: p5-params-validate p5-monalisa-apmon
Requires p5-clone p5-json-xs p5-mail-rfc822-address
# Actually, it is p5-xml-parser that requires this, but it doesn't configure itself correctly
# This is so it gets into our dependencies-setup.sh
Requires: expat

# Provided by system perl
Provides: perl(HTML::Entities)
Provides: perl(DB_File)
Provides: perl(Date::Manip)
Provides: perl(XML::LibXML)

# Fake for obsolete CLI/SiteDataInfo.pm
Provides: (XML::Twig)
# Fake provide of twitter client; needs to be installed manually
Provides: perl(Net::Twitter::Lite)

%prep
%setup -n %{downloadn}-admin
rm -rf Build
rm -rf Contrib
rm -rf Documentation/ACAT2008
rm -rf Documentation/DC04PostMortem
rm -rf Documentation/DC04Stats
rm -rf Documentation/Grid2005
rm -rf Documentation/Updates
rm -rf Documentation/WebConfig
rm -rf Documentation/WebSite
rm -rf Documentation/WhitePapers
rm -rf Migration
rm -rf perl_lib/DMWMMON
rm -rf perl_lib/PHEDEX/Testbed
rm -rf perl_lib/PHEDEX/Web/API
rm -rf perl_lib/PHEDEX/Web/{C,D,F,U}*
rm -rf perl_lib/PHEDEX/Web/S{pooler,SLSpacw,TH}.pm
rm -rf PhEDExWeb
rm -rf Testbed
rm -rf Toolkit/DBS
rm -rf Toolkit/Management
rm -rf Toolkit/Peers
rm -rf Toolkit/Test
rm -rf Utilities/testSpace
rm -f  Utilities/WebServiceWrite.pl

%build

%install
mkdir -p %i/etc
tar -cf - * | (cd %i && tar -xf -)

# Set permissions
chmod 755 %i/Utilities/*

# Copy dependencies to dependencies-setup.sh
mkdir -p %i/etc/profile.d
for x in %pkgreqs; do
 case $x in /* ) continue ;; esac
 p=%{instroot}/%{cmsplatf}/$(echo $x | sed 's/\([^+]*\)+\(.*\)+\([A-Z0-9].*\)/\1 \2 \3/' | tr ' ' '/')
 echo ". $p/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
 echo "source $p/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
done

# Make "env.sh" = "init.sh" for legacy configs
echo ". %i/etc/profile.d/init.sh" > %i/etc/profile.d/env.sh
echo "source %i/etc/profile.d/init.csh" > %i/etc/profile.d/env.csh

%post
%{relocateConfig}etc/profile.d/env.sh
%{relocateConfig}etc/profile.d/env.csh
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
