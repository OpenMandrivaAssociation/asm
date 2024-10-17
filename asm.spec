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

Summary:	A code manipulation tool to implement adaptable systems
Name:           asm
Epoch:          0
Version:        1.5.3
Release:        3.0.13
License:        BSD-style
Url:            https://asm.objectweb.org/
Group:		Development/Java
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

%description
ASM is a code manipulation tool to implement adaptable systems.

%package        javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java

%description        javadoc
Javadoc for %{name}.

%prep
%setup -q
%patch0 -p1
find . -name "*.jar" -exec rm -f {} \;
install -m 644 %{SOURCE1} .
install -m 644 %{SOURCE2} .

%build
%ant -Dobjectweb.ant.tasks.path=$(build-classpath objectweb-anttask) jar jdoc

%install
# jars
install -d -m 755 %{buildroot}%{_javadir}/%{name}
install -d -m 755 %{buildroot}%{_datadir}/maven2/poms

install -m 644 output/dist/lib/asm-%{version}.jar %{buildroot}%{_javadir}/%{name}/
install -m 644 %{SOURCE3} %{buildroot}%{_datadir}/maven2/poms/JPP.asm-asm.pom
%add_to_maven_depmap %{name} %{name} %{version} JPP/%{name} %{name}

install -m 644 output/dist/lib/asm-analysis-%{version}.jar %{buildroot}%{_javadir}/%{name}/
install -m 644 %{SOURCE4} %{buildroot}%{_datadir}/maven2/poms/JPP.asm-asm-analysis.pom
%add_to_maven_depmap %{name} %{name}-analysis %{version} JPP/%{name} %{name}-analysis

install -m 644 output/dist/lib/asm-attrs-%{version}.jar %{buildroot}%{_javadir}/%{name}/
install -m 644 %{SOURCE5} %{buildroot}%{_datadir}/maven2/poms/JPP.asm-asm-attrs.pom
%add_to_maven_depmap %{name} %{name}-attrs %{version} JPP/%{name} %{name}-attrs

install -m 644 output/dist/lib/asm-tree-%{version}.jar %{buildroot}%{_javadir}/%{name}/
install -m 644 %{SOURCE6} %{buildroot}%{_datadir}/maven2/poms/JPP.asm-asm-tree.pom
%add_to_maven_depmap %{name} %{name}-tree %{version} JPP/%{name} %{name}-tree

install -m 644 output/dist/lib/asm-util-%{version}.jar %{buildroot}%{_javadir}/%{name}/
install -m 644 %{SOURCE7} %{buildroot}%{_datadir}/maven2/poms/JPP.asm-asm-util.pom
%add_to_maven_depmap %{name} %{name}-util %{version} JPP/%{name} %{name}-util

install -m 644 output/dist/lib/asm-xml-%{version}.jar %{buildroot}%{_javadir}/%{name}/
install -m 644 %{SOURCE8} %{buildroot}%{_datadir}/maven2/poms/JPP.asm-asm-xml.pom
%add_to_maven_depmap %{name} %{name}-xml %{version} JPP/%{name} %{name}-xml

install -m 644 output/dist/lib/kasm-%{version}.jar %{buildroot}%{_javadir}/%{name}/
install -m 644 %{SOURCE9} %{buildroot}%{_datadir}/maven2/poms/JPP.asm-kasm.pom
%add_to_maven_depmap %{name} k%{name} %{version} JPP/%{name} k%{name}

for jar in output/dist/lib/*.jar; do
install -m 644 ${jar} \
%{buildroot}%{_javadir}/%{name}/`basename ${jar}`
done

(cd %{buildroot}%{_javadir}/%{name} && for jar in *-%{version}*; do \
ln -sf ${jar} ${jar/-%{version}/}; done)

# javadoc
install -p -d -m 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr output/dist/doc/javadoc/user/* %{buildroot}%{_javadocdir}/%{name}-%{version}
(cd %{buildroot}%{_javadocdir} && ln -sf %{name}-%{version} %{name})

%{__perl} -pi -e 's/\r$//g' README.txt

%{gcj_compile}

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
%doc README.txt faq.html asm-eng.pdf
%dir %{_javadir}/%{name}
%{_javadir}/%{name}/*.jar
%{_datadir}/maven2
%{_mavendepmapfragdir}
%{gcj_files}

%files javadoc
%dir %{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}-%{version}/*
%dir %{_javadocdir}/%{name}

