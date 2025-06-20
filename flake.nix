{
  # https://github.com/NixOS/nixpkgs/blob/49829a9adedc4d2c1581cc9a4294ecdbff32d993/doc/languages-frameworks/python.section.md#how-to-consume-python-modules-using-pip-in-a-virtual-environment-like-i-am-used-to-on-other-operating-systems-how-to-consume-python-modules-using-pip-in-a-virtual-environment-like-i-am-used-to-on-other-operating-systems
  # https://github.com/the-nix-way/dev-templates/blob/main/python/flake.nix
  # https://github.com/gmodena/flake-templates/blob/19af70e17e9aa8158bd4f0f1780035746329c2b9/python/flake.nix

  description = "Python development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.05";
  };

  outputs = {nixpkgs, ...}: let
    system = "x86_64-linux";
    pkgs = import nixpkgs {inherit system;};
  in {
    devShells.${system} = let
      python = pkgs.python311;
      pythonPackages = python.pkgs;
      # A set of system dependencies for Python modules.
      # They act as build inputs and are used to configure
      # LD_LIBRARY_PATH in the shell.
      systemPackages = with pkgs; [
        # Required by CQ-editor.
        zlib
        xorg.libxcb

        # Required when script is executed with python.
        stdenv.cc.cc.lib
        xorg.libX11
        xorg.libXrender
        expat

        # Required in both situations.
        libGL

        # May be required in the future.
        #xorg.libXi
        #glib
        #kdePackages.qtbase
        #libsForQt5.qt5.wrapQtAppsHook
        #libsForQt5.qt5.qtwayland
      ];
      yacv-frontend = pkgs.fetchzip {
        url = "https://github.com/yeicor-3d/yet-another-cad-viewer/releases/download/v0.9.3/frontend.zip";
        sha256 = "sha256-d5qKs9h4q9/hquVgWFb10KSE2gWTSAZQgYo9l0bzdVM=";
      };
    in {
      default = pkgs.mkShell {
        venvDir = ".venv";

        buildInputs =
          [
            yacv-frontend
            pkgs.ungoogled-chromium

            # A Python interpreter including the 'venv' module is required to bootstrap the environment.
            pythonPackages.python
            # This execute some shell code to initialize a venv in $venvDir before dropping into the shell
            pythonPackages.venvShellHook

            # Add below dependencies that we would like to use from nixpkgs, which will add them to
            #  PYTHONPATH and thus make them accessible from within the venv.
            pythonPackages.numpy

            pythonPackages.pip

            pkgs.nodejs_24 # For pyright
            # pythonPackages.python-lsp-server
            # pythonPackages.python-lsp-ruff
            # pythonPackages.pylsp-mypy
            # pythonPackages.pylsp-rope
          ]
          ++ systemPackages;

        # Run this command, only after creating the virtual environment
        postVenvCreation = ''
          unset SOURCE_DATE_EPOCH
        '';

        # Now we can execute any commands within the virtual environment.
        # This is optional and can be left out to run pip manually.

        postShellHook = ''
          unset SOURCE_DATE_EPOCH

          export LD_LIBRARY_PATH=${pkgs.lib.makeLibraryPath systemPackages}
          # https://discourse.nixos.org/t/python-qt-qpa-plugin-could-not-find-xcb/8862
          #export QT_QPA_PLATFORM_PLUGIN_PATH="{pkgs.kdePackages.qtbase}/lib/qt-6/plugins/platforms"
          #export QT_QPA_PLATFORM="minimal"

          alias yacv-frontend="nohup ${pkgs.writeShellScript "yacv-frontend" ''
            python -m http.server -d ${yacv-frontend} &
            P1=$!
            chromium --app="http://0.0.0.0:8000"
            kill $P1
          ''} &"

          pip install -q -r requirements.txt

          echo
          echo 'Run "yacv-frontend" or go to "https://yeicor-3d.github.io/yet-another-cad-viewer" to open the interface to view CAD models.'
          echo 'Run "python <file-with-build123d-cad-models>.py" to build and show the models.'
          echo 'Run ":!python %" in NVIM to run the current file with python.'
          echo
        '';
      };
    };
  };
}
