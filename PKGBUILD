_name="ebt"
_module="ebt"

pkgname=("python-${_module}")
pkgver="0.67"
pkgrel="1"
pkgdesc="Enchanced backup tool"
arch=("any")
url="https://github.com/larrabee/ebt"
license=("GPL")
depends=('python-configobj' 'rsync' 'btrfs-progs')
source=("https://github.com/larrabee/ebt/archive/${pkgver}.zip")
backup=('etc/ebt/ebt.conf' 'etc/ebt/plans.py')
md5sums=('eef466266f2023612260be149d83d579')

prepare() {
  echo "prepare"
}

package() {
  mkdir -p ${pkgdir}/usr/lib/python3.5/site-packages/ebt/
  mkdir -p ${pkgdir}/etc/ebt
  mkdir -p ${pkgdir}/usr/bin
  cp -r ${srcdir}/ebt-${pkgver}/code/* ${pkgdir}/usr/lib/python3.5/site-packages/ebt/
  cp -r ${srcdir}/ebt-${pkgver}/conf/* ${pkgdir}/etc/ebt/
  ln -s /usr/lib/python3.5/site-packages/ebt/ebt.py ${pkgdir}/usr/bin/ebt
}
