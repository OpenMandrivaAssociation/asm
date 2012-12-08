# Copyright (c) 2000-2008, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define gcj_support     1
%define section         free

Name:           asm
Version:        1.5.3
Release:        %mkrel 3.0.6
Epoch:          0
Summary:        A code manipulation tool to implement adaptable systems
License:        BSD-style
URL:            http://asm.objectweb.org/
Group:          Development/Java
Source0:        http://download.us.forge.objectweb.org/asm/asm-1.5.3.tar.gz
Source1:        http://asm.objectweb.org/current/asm-eng.pdf
Source2:        http://asm.objectweb.org/doc/faq.html
Source3:        http://repo1.maven.org/maven2/asm/asm/1.5.3/asm-1.5.3.pom
Source4:        http://repo1.maven.org/maven2/asm/asm-analysis/1.5.3/asm-analysis-1.5.3.pom
Source5:        http://repo1.maven.org/maven2/asm/asm-attrs/1.5.3/asm-attrs-1.5.3.pom
Source6:        http://repo1.maven.org/maven2/asm/asm-tree/1.5.3/asm-tree-1.5.3.pom
Source7:        http://repo1.maven.org/maven2/asm/asm-util/1.5.3/asm-util-1.5.3.pom
Source8:        http://repo1.maven.org/maven2/asm/asm-xml/1.5.3/asm-xml-1.5.3.pom
Source9:        http://repo1.maven.org/maven2/asm/kasm/1.5.3/kasm-1.5.3.pom
Patch0:         asm-no-classpath-in-manifest.patch
BuildRequires:  ant
BuildRequires:  java-devel
BuildRequires:  java-rpmbuild >= 0:1.6
BuildRequires:  objectweb-anttask
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel >= 0:1.0.31
%else
BuildArch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
ASM is a code manipulation tool to implement adaptable systems.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description        javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1
find . -name "*.jar" -exec rm -f {} \;
install -m 644 %{SOURCE1} .
install -m 644 %{SOURCE2} .

%build
%ant -Dobjectweb.ant.tasks.path=$(build-classpath objectweb-anttask) jar jdoc

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/%{name}
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms

install -m 644 output/dist/lib/asm-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.asm-asm.pom
%add_to_maven_depmap %{name} %{name} %{version} JPP/%{name} %{name}

install -m 644 output/dist/lib/asm-analysis-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.asm-asm-analysis.pom
%add_to_maven_depmap %{name} %{name}-analysis %{version} JPP/%{name} %{name}-analysis

install -m 644 output/dist/lib/asm-attrs-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.asm-asm-attrs.pom
%add_to_maven_depmap %{name} %{name}-attrs %{version} JPP/%{name} %{name}-attrs

install -m 644 output/dist/lib/asm-tree-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/
install -m 644 %{SOURCE6} $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.asm-asm-tree.pom
%add_to_maven_depmap %{name} %{name}-tree %{version} JPP/%{name} %{name}-tree

install -m 644 output/dist/lib/asm-util-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.asm-asm-util.pom
%add_to_maven_depmap %{name} %{name}-util %{version} JPP/%{name} %{name}-util

install -m 644 output/dist/lib/asm-xml-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/
install -m 644 %{SOURCE8} $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.asm-asm-xml.pom
%add_to_maven_depmap %{name} %{name}-xml %{version} JPP/%{name} %{name}-xml

install -m 644 output/dist/lib/kasm-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/
install -m 644 %{SOURCE9} $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.asm-kasm.pom
%add_to_maven_depmap %{name} k%{name} %{version} JPP/%{name} k%{name}



for jar in output/dist/lib/*.jar; do
install -m 644 ${jar} \
$RPM_BUILD_ROOT%{_javadir}/%{name}/`basename ${jar}`
done

(cd $RPM_BUILD_ROOT%{_javadir}/%{name} && for jar in *-%{version}*; do \
ln -sf ${jar} ${jar/-%{version}/}; done)

# javadoc
install -p -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr output/dist/doc/javadoc/user/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
(cd $RPM_BUILD_ROOT%{_javadocdir} && ln -sf %{name}-%{version} %{name})

%{__perl} -pi -e 's/\r$//g' README.txt

%{gcj_compile}

%clean
%{__rm} -rf %{buildroot}


%post
%update_maven_depmap
%if %{gcj_support}
%{update_gcjdb}
%endif

%postun
%update_maven_depmap
%if %{gcj_support}
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc README.txt faq.html asm-eng.pdf
%dir %{_javadir}/%{name}
%{_javadir}/%{name}/*.jar
%{_datadir}/maven2
%{_mavendepmapfragdir}
%{gcj_files}

%files javadoc
%defattr(0644,root,root,0755)
%dir %{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}-%{version}/*
%dir %{_javadocdir}/%{name}




%changelog
* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 0:1.5.3-3.0.6mdv2011.0
+ Revision: 662791
- mass rebuild

* Mon Nov 29 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.5.3-3.0.5mdv2011.0
+ Revision: 603185
- rebuild

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.5.3-3.0.4mdv2010.1
+ Revision: 522090
- rebuilt for 2010.1

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 0:1.5.3-3.0.3mdv2010.0
+ Revision: 413039
- rebuild

* Fri Mar 06 2009 Antoine Ginies <aginies@mandriva.com> 0:1.5.3-3.0.2mdv2009.1
+ Revision: 349993
- 2009.1 rebuild

* Mon Feb 18 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0:1.5.3-3.0.1mdv2008.1
+ Revision: 172094
- add maven poms and depmaps

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:1.5.3-2.4mdv2008.1
+ Revision: 120828
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:1.5.3-2.3mdv2008.0
+ Revision: 87201
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Tue Jul 03 2007 Anssi Hannula <anssi@mandriva.org> 0:1.5.3-2.2mdv2008.0
+ Revision: 47576
- rebuild for new libgcj


* Sat Dec 16 2006 David Walluck <walluck@mandriva.org> 1.5.3-2.1mdv2007.0
+ Revision: 97984
- Import asm

* Fri Dec 15 2006 David Walluck <walluck@mandriva.org> 0:1.5.3-2.1mdv2007.1
- gcj_support

* Sun Jan 15 2006 David Walluck <walluck@mandriva.org> 0:1.5.3-1.2mdk
- BuildRequires: java-devel

* Mon Sep 12 2005 David Walluck <walluck@mandriva.org> 0:1.5.3-1.1mdk
- release

* Fri Jul 01 2005 Gary Benson <gbenson@redhat.com> 0:1.5.3-1jpp_1fc
- Build into Fedora.

* Fri May 06 2005 Fernando Nasser <fnasser@redhat.com> 0:1.5.3-1jpp_1rh
- Merge with upstream for upgrade

* Fri Mar 11 2005 Sebastiano Vigna <vigna at acm.org> 0:1.5.3-1jpp
- Upgrade to 1.5.3

* Tue Feb 01 2005 Ralph Apel <r.apel at r-apel.de> 0:1.4.3-1jpp
- Upgrade to 1.4.3
- Require objectweb-anttask instead of owanttask

* Mon Nov 15 2004 Fernando Nasser <fnasser@redhat.com> 0:1.4.1-4jpp_1rh
- First Red Hat build

* Tue Sep 21 2004 Ralph Apel <r.apel at r-apel.de> 0:1.4.1-4jpp
- Require owanttask instead of monolog

* Sat Aug 21 2004 Ralph Apel <r.apel at r-apel.de> 0:1.4.1-3jpp
- Build with ant-1.6.2

* Sun Feb 08 2004 David Walluck <david@anti-microsoft.org> 0:1.4.1-2jpp
- this release uses new upstream tarball from author
- add some documentation from website

* Thu Jan 22 2004 David Walluck <david@anti-microsoft.org> 0:1.4.1-1jpp
- release

