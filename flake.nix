{
  description = "Get Oodle library for Unreal Engine";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs?ref=nixos-unstable";
  };

  outputs =
    { nixpkgs, ... }:
    let
      inherit (nixpkgs) lib;

      supportedSystems = [
        "x86_64-linux"
      ];

      forAllSystems =
        f:
        lib.genAttrs supportedSystems (
          system:
          f (
            import nixpkgs {
              inherit system;
            }
          )
        );
    in
    {
      devShells = forAllSystems (pkgs: {
        default = pkgs.mkShell {
          nativeBuildInputs = [
            pkgs.python3
            pkgs.poetry
          ];

          # https://github.com/NixOS/nix/issues/12234
          shellHook = ''
            export SSL_CERT_FILE="${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt"
          '';
        };
      });
    };
}
