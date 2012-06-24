%define	mod_name	auth_any
%define apxs		/usr/sbin/apxs
Summary:	Basic authentication for the Apache Web server using arbitrary shell commands
Summary(cs.UTF-8):	Základní autentizace pro WWW server Apache pomocí shellových příkazů
Summary(da.UTF-8):	En autenticeringsmodul for webtjeneren Apache hvor man kan bruge vilkårlige skal-kommandoer
Summary(de.UTF-8):	Authentifizierung für den Apache Web-Server, der arbiträre Shell-Befehle verwendet
Summary(fr.UTF-8):	Authentification de base pour le serveur Web Apache utilisant des commandes shell arbitraires
Summary(it.UTF-8):	Autenticazione di base per il server Web Apache mediante comandi arbitrari della shell
Summary(nb.UTF-8):	En autentiseringsmodul for webtjeneren Apache der en kan bruke skall-kommandoer
Summary(pl.UTF-8):	Podstawowy moduł uwierzytelnienia dla Apache, używający poleceń powłoki
Summary(pt.UTF-8):	Um módulo de autenticação de LDAP para o servidor Web Apache
Summary(sl.UTF-8):	Osnovna avtentikacija za spletni strežnik Apache, z uporabo poljubnih lupinskih ukazov
Summary(sv.UTF-8):	Grundläggande autentisering för webbservern Apache med valfria skalkommandon
Name:		apache-mod_%{mod_name}
Version:	1.6
Release:	0.rc1.1
Epoch:		1
License:	BSD
Group:		Networking/Daemons
Source0:	http://www.itlab.musc.edu/webNIS/dist/mod_%{mod_name}-%{version}-rc1.tar.gz
# Source0-md5:	76a105e42fb82947c2c4243975a1b7f9
Patch0:		%{name}-conf.patch
URL:		http://www.itlab.musc.edu/webNIS/mod_auth_any.html
BuildRequires:	apache-apxs >= 2.0
BuildRequires:	apache-devel >= 2.0
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
This module allows you to use any command line program (such as
webNIS) to authenticate a user.

%description -l cs.UTF-8
Balíček mod_auth_any slouží pro omezení přístupu k dokumentům, které
poskytuje WWW server Apache. Jména a hesla jsou kontrolována pomocí
jakéhokoliv příkazu (jeho návratovým kódem).

%description -l de.UTF-8
Mod_auth_any kann verwendet werden, um den Zugriff auf von einem Web-
Server bediente Dokumente zu beschränken, indem es den Rückcode eines
gegebenen arbiträren Befehls prüft.

%description -l es.UTF-8
Mod_auth_any puede usarse para limitar el acceso a documentos servidos
desde un servidor web verificando el código de retorno de un comando
arbitrario especificado.

%description -l fr.UTF-8
Mod_auth_any peut être utilisé pour limiter l'accès à des documents
servis par un serveur Web en vérifiant le code de retour d'une
commande spécifiée arbitraire.

%description -l it.UTF-8
Mod_auth_any può essere utilizzato per limitare l'accesso ai documenti
serviti da un server Web controllando il codice di ritorno di un dato
comando arbitrario.

%description -l ja.UTF-8
Mod_auth_any は任意に指定されたコマンドの戻りコードをチェックすること
によって、Web サーバーが提供するドキュメントへのアクセスを制限すること
ができます。

%description -l pl.UTF-8
Ten moduł pozwala na użycie dowolnego programu działającego z linii
poleceń (jak np. webNIS) do uwierzytelniania użytkownika.

%description -l sv.UTF-8
Mod_auth_any kan användas för att begränsa åtkomsten till dokument
servade av en webbserver genom att kontrollera returkoden från ett
godtyckligt angivet kommando.

%prep
%setup -q -n mod_%{mod_name}
%patch0 -p1

%build
%{__make} APXS2=/usr/sbin/apxs

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/httpd.conf}

install src/.libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
echo 'LoadModule %{mod_name}_module modules/mod_%{mod_name}.so' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc docs/* TODO
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
