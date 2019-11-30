defmodule Day9 do
  # An attempt to a bi-directional circular linked list implement with a
  # worst-case time complexity of O(1) (amortized)
  
  defp insert_r(circular_list, value) do
    # insert between curr and r
    Map.merge(circular_list, %{
      r: [value | circular_list[:r]],
      r_sz: circular_list[:r_sz] + 1,
    })
  end

  defp flip(circular_list) do
    Map.merge(circular_list, %{
      l: circular_list[:r],
      l_sz: circular_list[:r_sz],
      r: circular_list[:l],
      r_sz: circular_list[:l_sz],
    })
  end

  defp rot_l(circular_list) do
    flip(rot_r(flip(circular_list)))
  end

  defp balance_r(circular_list) do
    # assumption: r's already empty
    # edge case: when l_sz is 1, l shall be empty after balancing (ensuring
    # r's non-empty after the operation)
    new_l_sz = Kernel.div(circular_list[:l_sz], 2)
    {new_l, new_r_rev} = Enum.split(circular_list[:l], new_l_sz)
    Map.merge(circular_list, %{
      l: new_l,
      l_sz: new_l_sz,
      r: Enum.reverse(new_r_rev),
      r_sz: circular_list[:l_sz] - new_l_sz,
    })
  end

  defp rot_r(circular_list) do
    cond do
      circular_list[:r_sz] > 0 ->
        %{
          curr: Kernel.hd(circular_list[:r]),
          l: [circular_list[:curr] | circular_list[:l]],
          l_sz: circular_list[:l_sz] + 1,
          r: Kernel.tl(circular_list[:r]),
          r_sz: circular_list[:r_sz] - 1,
        }
      circular_list[:r_sz] == 0 ->
        cond do
          circular_list[:l_sz] == 0 ->
            circular_list
          circular_list[:l_sz] == 1 ->
            %{
              curr: Kernel.hd(circular_list[:l]),
              l: [],
              l_sz: 0,
              r: [circular_list[:curr]],
              r_sz: 1,
            }
          circular_list[:l_sz] > 1 ->
            rot_r(balance_r(circular_list))
        end
    end
  end

  defp pop_r(circular_list) do
    # pops curr and picks hd(r) as the new curr
    circular_list = if circular_list[:r_sz] == 0 do
      balance_r(circular_list)
    else
      circular_list
    end
    {circular_list[:curr], Map.merge(circular_list, %{
      curr: Kernel.hd(circular_list[:r]),
      r: Kernel.tl(circular_list[:r]),
      r_sz: circular_list[:r_sz] - 1,
    })}
  end

  def max_score(n_player, n_marble) do
    circular_list = %{
      curr: 0,
      l: [],  # counter-clockwise
      l_sz: 0,
      r: [],  # clockwise
      r_sz: 0,
    }
    player_score = for _ <- 0..n_marble, do: 0  # Updating costs O(n). Well, not unacceptable, though.
    Enum.reduce(1..n_marble, {circular_list, player_score}, fn(marble_id, {circular_list, player_score}) -> 
      player = rem(marble_id - 1, n_player) + 1
      cond do
        rem(marble_id, 23) != 0 ->
          {rot_r(insert_r(rot_r(circular_list), marble_id)), player_score}
        rem(marble_id, 23) == 0 ->
          circular_list = Enum.reduce(1..7, circular_list, fn(_, circular_list) ->
            rot_l(circular_list)
          end)
          {removed, circular_list} = pop_r(circular_list)
          player_score = List.update_at(player_score, player, fn score -> score + removed + marble_id end)
          {circular_list, player_score}
      end
    end) |> (fn {_, player_score} -> player_score end).() |> Enum.max
  end
end

IO.gets("")
  |> String.trim
  |> String.split(" ")
  |> Enum.map(&Integer.parse/1)
  |> Enum.map(fn x -> Kernel.elem(x, 0) end)
  |> (fn [x, y] -> Day9.max_score(x, y) end).()
  |> IO.puts
