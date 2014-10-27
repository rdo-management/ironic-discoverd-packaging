%{?!_licensedir:%global license %%doc}

Name:		openstack-ironic-discoverd
Summary:	Hardware property discovery service for OpenStack Ironic
Version:	0.2.2
Release:	1%{?dist}
License:	ASL 2.0
Group:		System Environment/Base
URL:		https://github.com/Divius/ironic-discoverd

Source0:	https://pypi.python.org/packages/source/i/ironic-discoverd/ironic-discoverd-%{version}.tar.gz
Source1:	openstack-ironic-discoverd.service
Source2:	openstack-ironic-discoverd-dnsmasq.service
Source3:	dnsmasq.conf

BuildArch:	noarch
BuildRequires:	python-setuptools
BuildRequires:	python2-devel
BuildRequires:	systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Requires: python-eventlet
Requires: python-flask
Requires: python-ironicclient
Requires: python-keystoneclient
Requires: python-requests
Requires: python-six
Requires: dnsmasq


%prep
%autosetup -n ironic-discoverd-%{version}
rm -rf *.egg-info

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root=%{buildroot}
mkdir -p %{buildroot}%{_mandir}/man8
install -p -D -m 644 ironic-discoverd.8 %{buildroot}%{_mandir}/man8/

# install systemd scripts
mkdir -p %{buildroot}%{_unitdir}
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}

# configuration contains passwords, thus 640
install -p -D -m 640 example.conf %{buildroot}/%{_sysconfdir}/ironic-discoverd/discoverd.conf
install -p -D -m 644 %{SOURCE3} %{buildroot}/%{_sysconfdir}/ironic-discoverd/dnsmasq.conf


%description
Hardware properties discovery daemon for use with OpenStack Ironic.

%files
%doc README.rst
%license LICENSE
%{python_sitelib}/ironic_discoverd*
%config(noreplace) %attr(-,root,root) %{_sysconfdir}/ironic-discoverd
%{_bindir}/ironic-discoverd
%{_unitdir}/openstack-ironic-discoverd.service
%{_unitdir}/openstack-ironic-discoverd-dnsmasq.service
%doc %{_mandir}/man8/ironic-discoverd.8.gz

%post
%systemd_post openstack-ironic-discoverd.service
%systemd_post openstack-ironic-discoverd-dnsmasq.service

%preun
%systemd_preun openstack-ironic-discoverd.service
%systemd_preun openstack-ironic-discoverd-dnsmasq.service

%postun
%systemd_postun_with_restart openstack-ironic-discoverd.service
%systemd_postun_with_restart openstack-ironic-discoverd-dnsmasq.service


%changelog

* Mon Oct 27 2014 Dmitry Tantsur <dtantsur@redhat.com> - 0.2.2-1
- Upstream bugfix release 0.2.2
- Sync all descriptions with upstream variant

* Thu Oct 23 2014 Dmitry Tantsur <dtantsur@redhat.com> - 0.2.1-2
- Require dnsmasq
- Add openstack-ironic-discoverd-dnsmasq.service - sample service for dnsmasq
- Updated description to upstream version

* Thu Oct 16 2014 Dmitry Tantsur <dtantsur@redhat.com> - 0.2.1-1
- Upstream bugfix release

* Wed Oct 8 2014 Dmitry Tantsur <dtantsur@redhat.com> - 0.2.0-1
- Initial package build

