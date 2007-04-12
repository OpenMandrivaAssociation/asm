# Copyright (c) 2000-2005, JPackage Project
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
Release:        %mkrel 2.1
Epoch:          0
Summary:        A code manipulation tool to implement adaptable systems
License:        BSD-style
URL:            http://asm.objectweb.org/
Group:          Development/Java
Source0:        http://download.us.forge.objectweb.org/asm/asm-1.5.3.tar.gz
Source1:        http://asm.objectweb.org/current/asm-eng.pdf
Source2:        http://asm.objectweb.org/doc/faq.html
Patch0:         asm-no-classpath-in-manifest.patch
BuildRequires:  ant
BuildRequires:  java-devel
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  objectweb-anttask
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel >= 0:1.0.31
Requires(post): java-gcj-compat >= 0:1.0.31
Requires(postun): java-gcj-compat >= 0:1.0.31
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

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
%{__rm} -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ $1 -eq 0 ]; then
  rm -f %{_javadocdir}/%{name}
fi

%files
%defattr(0644,root,root,0755)
%doc README.txt faq.html asm-eng.pdf
%dir %{_javadir}/%{name}
%{_javadir}/%{name}/*.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%dir %{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}-%{version}/*
%ghost %dir %{_javadocdir}/%{name}


