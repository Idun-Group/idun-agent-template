# Use test Idun engine package

## On idun-agent-platform

cd /Users/geoffreyharrazi/Documents/GitHub/idun-agent-platform
cd libs/idun_agent_schema
uv build --no-sources
cd ../idun_agent_engine
uv build --no-sources

## On the test project

python -m pip install --upgrade pip
python -m pip install \
  /Users/geoffreyharrazi/Documents/GitHub/idun-agent-platform/libs/idun_agent_engine/dist/*.whl

OLD:
python -m pip install --upgrade pip
python -m pip install \
  /Users/geoffreyharrazi/Documents/GitHub/idun-agent-platform/libs/idun_agent_schema/dist/*.whl \
  /Users/geoffreyharrazi/Documents/GitHub/idun-agent-platform/libs/idun_agent_engine/dist/*.whl

### Test

python -c "import idun_agent_engine; import idun_platform_cli; print(idun_agent_engine.__file__)"
idun --help