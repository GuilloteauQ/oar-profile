with (import <nixpkgs>{});

let
  app_name = "oar-profile";
  app_version = "1.0";
in {
  ctrl_email = python37Packages.buildPythonPackage rec {
    name = "${app_name}";
    version = "${app_version}";

    # src = fetchTarball("https://github.com/GuilloteauQ/oar-profile/tarball/main");
    src = ./.;
    propagatedBuildInputs = with python37Packages; [
    ];

    doCheck = false;

    postInstall = ''
      cp -r app/ $out
    '';
  };
}
