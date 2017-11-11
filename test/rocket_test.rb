require 'minitest/autorun'
require './app/rocket'

class RocketTest < MiniTest::Unit::TestCase

  def setup
    @rocket = Rocket.new
  end

  def rocket_initial_state_is_ground
    assert_equal "ground", @rocket.state
  end
end
