{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python3
    python3Packages.pandas
    python3Packages.openpyxl
    python3Packages.pyyaml
  ];

  shellHook = ''
    echo "Python environment with pandas, openpyxl, and pyyaml ready"
  '';
}