%define	mod_name	auth_any
%define apxs		/usr/sbin/apxs
Summary:	Basic authentication for the Apache Web server using arbitrary shell commands
Summary(cs):	Z�kladn� autentizace pro WWW server Apache pomoc� shellov�ch p��kaz�
Summary(da):	En autenticeringsmodul for webtjeneren Apache hvor man kan bruge vilk�rlige skal-kommandoer
Summary(de):	Authentifizierung f�r den Apache Web-Server, der arbitr�re Shell-Befehle verwendet
Summary(fr):	Authentification de base pour le serveur Web Apache utilisant des commandes shell arbitraires
Summary(it):	Autenticazione di base per il server Web Apache mediante comandi arbitrari della shell
Summary(nb):	En autentiseringsmodul for webtjeneren Apache der en kan bruke skall-kommandoer
Summary(pl):	Podstawowy modu� uwierzytelnienia dla Apache, u�ywaj�cy polece� pow�oki
Summary(pt):	Um m�dulo de autentica��o de LDAP para o servidor Web Apache
Summary(sl):	Osnovna avtentikacija za spletni stre�nik Apache, z uporabo poljubnih lupinskih ukazov
Summary(sv):	Grundl�ggande autentisering f�r webbservern Apache med valfria skalkommandon
Name:		apache-mod_%{mod_name}
Version:	1.2.2
Release:	1
Epoch:		1
License:	BSD
Group:		Networking/Daemons
Source0:	http://www.itlab.musc.edu/webNIS/dist/mod_%{mod_name}-%{version}-apache2.tar.gz
# Source0-md5:	e9a1825b818d108e1204692da3d7bfd0
URL:		http://www.itlab.musc.edu/webNIS/mod_auth_any.html
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2
Requires(post,preun):	%{apxs}
Requires:	apache >= 2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)

%description
This module allows you to use any command line program (such as
webNIS) to authenticate a user.

%description -l cs
Bal��ek mod_auth_any slou�� pro omezen� p��stupu k dokument�m, kter�
poskytuje WWW server Apache. Jm�na a hesla jsou kontrolov�na pomoc�
jak�hokoliv p��kazu (jeho n�vratov�m k�dem).

%description -l de
Mod_auth_any kann verwendet werden, um den Zugriff auf von einem Web-
Server bediente Dokumente zu beschr�nken, indem es den R�ckcode eines
gegebenen arbitr�ren Befehls pr�ft.

%description -l es
Mod_auth_any puede usarse para limitar el acceso a documentos servidos
desde un servidor web verificando el c�digo de retorno de un comando
arbitrario especificado.

%description -l fr
Mod_auth_any peut �tre utilis� pour limiter l'acc�s � des documents
servis par un serveur Web en v�rifiant le code de retour d'une
commande sp�cifi�e arbitraire.

%description -l it
Mod_auth_any pu� essere utilizzato per limitare l'accesso ai documenti
serviti da un server Web controllando il codice di ritorno di un dato
comando arbitrario.

%description -l ja
Mod_auth_any ��Ǥ�դ˻��ꤵ�줿���ޥ�ɤ���ꥳ���ɤ�����å����뤳��
�ˤ�äơ�Web �����С����󶡤���ɥ�����ȤؤΥ������������¤��뤳��
���Ǥ��ޤ���

%description -l pl
Ten modu� pozwala na u�ycie dowolnego programu dzia�aj�cego z linii
polece� (jak np. webNIS) do uwierzytelniania u�ytkownika.

%description -l sv
Mod_auth_any kan anv�ndas f�r att begr�nsa �tkomsten till dokument
servade av en webbserver genom att kontrollera returkoden fr�n ett
godtyckligt angivet kommando.

%prep
%setup -q -n mod_%{mod_name}-%{version}-apache2

%build
%{apxs} -c src/mod_%{mod_name}.c -o mod_%{mod_name}.so -Wl,-shared

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkglibdir}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{apxs} -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc docs/*
%attr(755,root,root) %{_pkglibdir}/*
