{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      supportedSystems = nixpkgs.lib.filterAttrs
        (system: _: system == "aarch64-darwin")
        nixpkgs.legacyPackages;
    in
    {
      devShells = builtins.mapAttrs
        (system: pkgs:
          {
            default = pkgs.mkShell {
              packages = with pkgs; [
                uv
                python313
              ];
            };
          })
        supportedSystems;
    };
}
