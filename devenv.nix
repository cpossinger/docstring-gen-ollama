{ pkgs, ... }:
{
  packages = [ pkgs.ollama ];

  languages.python = {
    enable = true;
    version = "3.12";
    uv.enable = true;
    venv.enable = true;
    venv.requirements = ''
      hatch
      ollama
      tqdm
    '';
  };
}
