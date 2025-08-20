{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    nodejs_20
  ];

  shellHook = ''
    echo "Roon Export Tags Development Environment"
    echo "Node.js version: $(node --version)"
    echo "NPM version: $(npm --version)"
    echo ""
    echo "To get started:"
    echo "  npm install"
    echo "  npm start [output-file.yaml]"
  '';
}